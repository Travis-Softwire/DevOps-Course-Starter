from flask import Flask, render_template, redirect, request

from todo_app.constants import COMPLETED, NOT_STARTED
from todo_app.data.trello_items import get_items, add_item, update_status, delete_item
from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config())


@app.route('/')
def index():
    return render_template('index.html', items=get_items(), not_started_status=NOT_STARTED)


@app.route('/add', methods=['POST'])
def add_to_do():
    add_item(request.form.get('title'), request.form.get('description'), request.form.get('due-date'))
    return redirect('/')


@app.route('/complete', methods=['POST'])
def complete_to_do():
    current_item_id = request.form.get('item-id')
    update_status(current_item_id, COMPLETED)
    return redirect('/')


@app.route('/uncomplete', methods=['POST'])
def uncomplete_to_do():
    current_item_id = request.form.get('item-id')
    update_status(current_item_id, NOT_STARTED)
    return redirect('/')


@app.route('/delete', methods=['POST'])
def delete_to_do():
    delete_item(request.form.get('item-id'))
    return redirect('/')
