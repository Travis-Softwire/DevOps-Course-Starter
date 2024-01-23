from flask import Flask, render_template, redirect, request

from todo_app.flask_config import Config
from todo_app.data.session_items import get_items, add_item, get_item, save_item, delete_item

app = Flask(__name__)
app.config.from_object(Config())


@app.route('/')
def index():
    return render_template('index.html', items=get_items())


@app.route('/add', methods=['POST'])
def add_to_do():
    add_item(request.form.get('title'))
    return redirect('/')


@app.route('/complete', methods=['POST'])
def complete_to_do():
    current_item = get_item(request.form.get('item-id'))
    current_item['status'] = 'Completed'
    save_item(current_item)
    return redirect('/')


@app.route('/delete', methods=['POST'])
def delete_to_do():
    delete_item(request.form.get('item-id'))
    return redirect('/')
