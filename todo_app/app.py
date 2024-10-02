from flask import Flask, render_template, redirect, request

from todo_app.constants import COMPLETED, NOT_STARTED
from todo_app.data.cosmos_item_repository import CosmosItemRepository
from todo_app.data.view_model import ViewModel
from todo_app.flask_config import Config


def create_app():
    todo_app = Flask(__name__)
    todo_app.config.from_object(Config)

    repo = CosmosItemRepository()

    @todo_app.route('/')
    def index():
        item_view_model = ViewModel(repo.get_items())
        return render_template('index.html', view_model=item_view_model, not_started_status=NOT_STARTED)

    @todo_app.route('/add', methods=['POST'])
    def add_to_do():
        repo.add_item(request.form.get('title'), request.form.get('description'), request.form.get('due-date'))
        return redirect('/')

    @todo_app.route('/complete', methods=['POST'])
    def complete_to_do():
        current_item_id = request.form.get('item-id')
        repo.update_status(current_item_id, COMPLETED)
        return redirect('/')

    @todo_app.route('/uncomplete', methods=['POST'])
    def uncomplete_to_do():
        current_item_id = request.form.get('item-id')
        repo.update_status(current_item_id, NOT_STARTED)
        return redirect('/')

    @todo_app.route('/delete', methods=['POST'])
    def delete_to_do():
        repo.delete_item(request.form.get('item-id'))
        return redirect('/')

    return todo_app


app = create_app()



