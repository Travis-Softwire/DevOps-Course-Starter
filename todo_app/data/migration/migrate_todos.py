import importlib
import todo_app.data.cosmos_client
from todo_app.data.cosmos_item_repository import CosmosItemRepository
from todo_app.data.item import Item
from todo_app.data.migration.trello_items import TrelloItemRepository
from dotenv import find_dotenv, load_dotenv


def annotate_trello_item(item):
    trello_id = item.id
    annotation = f"Trello item id: {trello_id} - "
    new_description = annotation + item.description
    return Item(item.id, item.title, new_description, item.due_date, item.last_modified, item.status)


def is_same_item(cosmos_item, trello_item):
    check_string = f"Trello item id: {trello_item.id} - "
    return cosmos_item.description.startswith(check_string)


def migrate_todos():
    trello_repository = TrelloItemRepository()
    trello_items = trello_repository.get_items()
    annotated_trello_items = map(annotate_trello_item, trello_items)

    cosmos_repository = CosmosItemRepository()
    cosmos_items = cosmos_repository.get_items()

    for trello_item in annotated_trello_items:
        if not any(is_same_item(cosmos_item, trello_item) for cosmos_item in cosmos_items):
            new_id = cosmos_repository.add_item(trello_item.title, trello_item.description, trello_item.due_date)
            cosmos_repository.update_status(str(new_id.inserted_id), trello_item.status)


file_path = find_dotenv('./.env')
load_dotenv(file_path, override=True)
importlib.reload(todo_app.data.migration.trello_client)
importlib.reload(todo_app.data.cosmos_client)

migrate_todos()

