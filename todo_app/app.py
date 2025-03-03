from flask import Flask, render_template, redirect, request
from flask_login import current_user, login_required

from todo_app.auth.current_todo_user import get_current_user_id
from todo_app.auth.role_decorators import requires_role
from todo_app.auth.setup_auth import initialise_auth, login_callback_delegate
from todo_app.constants import COMPLETED, NOT_STARTED
from todo_app.data.cosmos_item_repository import CosmosItemRepository
from todo_app.data.cosmos_user_repository import CosmosUserRepository
from todo_app.data.todo_view_model import ToDoViewModel
from todo_app.data.user_management_view_model import UserManagementViewModel
from todo_app.flask_config import Config


def create_app():
    todo_app = Flask(__name__)
    todo_app.config.from_object(Config())

    items_repo = CosmosItemRepository()
    user_repo = CosmosUserRepository()

    @todo_app.route('/')
    @login_required
    @requires_role(['Reader'])
    def index():
        user_can_write = False
        for role in ['Admin', 'Writer']:
            if user_repo.does_user_have_role(get_current_user_id(), role):
                user_can_write = True
        item_view_model = ToDoViewModel(items_repo.get_items(), user_can_write)
        return render_template('index.html', view_model=item_view_model, not_started_status=NOT_STARTED)

    @todo_app.route('/users')
    @login_required
    @requires_role(['Admin'])
    def manage_users():
        cosmos_user_repository = CosmosUserRepository()
        users = cosmos_user_repository.get_users()
        view_model = UserManagementViewModel(users)
        return render_template('user.html', view_model=view_model)

    @todo_app.route('/add', methods=['POST'])
    @login_required
    @requires_role(['Writer', 'Admin'])
    def add_to_do():
        items_repo.add_item(request.form.get('title'), request.form.get('description'), request.form.get('due-date'))
        return redirect('/')

    @todo_app.route('/complete', methods=['POST'])
    @login_required
    @requires_role(['Writer', 'Admin'])
    def complete_to_do():
        current_item_id = request.form.get('item-id')
        items_repo.update_status(current_item_id, COMPLETED)
        return redirect('/')

    @todo_app.route('/uncomplete', methods=['POST'])
    @login_required
    @requires_role(['Writer', 'Admin'])
    def uncomplete_to_do():
        current_item_id = request.form.get('item-id')
        items_repo.update_status(current_item_id, NOT_STARTED)
        return redirect('/')

    @todo_app.route('/delete', methods=['POST'])
    @login_required
    @requires_role(['Writer', 'Admin'])
    def delete_to_do():
        items_repo.delete_item(request.form.get('item-id'))
        return redirect('/')

    @todo_app.route('/make-admin', methods=['POST'])
    @login_required
    @requires_role(['Admin'])
    def make_user_admin():
        user_repo.add_user_role(request.form.get('user-id'), 'Admin')
        return redirect('/users')

    @todo_app.route('/remove-admin', methods=['POST'])
    @login_required
    @requires_role(['Admin'])
    def remove_user_admin():
        user_repo.remove_user_role(request.form.get('user-id'), 'Admin')
        return redirect('/users')

    @todo_app.route('/make-writer', methods=['POST'])
    @login_required
    @requires_role(['Admin'])
    def make_user_writer():
        user_repo.add_user_role(request.form.get('user-id'), 'Writer')
        return redirect('/users')

    @todo_app.route('/remove-writer', methods=['POST'])
    @login_required
    @requires_role(['Admin'])
    def remove_user_writer():
        user_repo.remove_user_role(request.form.get('user-id'), 'Writer')
        return redirect('/users')

    @todo_app.route('/delete-user', methods=['POST'])
    @login_required
    @requires_role(['Admin'])
    def delete_user():
        user_repo.delete_user(request.form.get('user-id'))
        return redirect('/users')

    @todo_app.route('/login/callback')
    def login_callback():
        return login_callback_delegate()

    def access_denied(_):
        return render_template('forbidden.html')

    todo_app.register_error_handler(401, access_denied)
    todo_app.register_error_handler(403, access_denied)

    initialise_auth(todo_app)
    return todo_app


app = create_app()
