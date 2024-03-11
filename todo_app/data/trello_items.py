from todo_app.constants import NOT_STARTED
from todo_app.data.item import Item
from todo_app.data.trello_client import TrelloClient


def item_key(item):
    return item.status


def get_items():
    """
    Fetches all saved items from Trello.

    Returns:
        list: a sorted list of saved items.
    """
    trello_lists = TrelloClient.get_trello_lists()
    items = Item.items_from_trello_lists(trello_lists)

    return sorted(items, key=item_key)


def add_item(title, description, due_date):
    """
    Adds a new item with the specified title to the session.

    Args:
        title: The title of the item.

    """
    TrelloClient.create_trello_card(title, description, due_date, NOT_STARTED)


def update_status(card_id, status):
    """
    Updates the status of the item with the specified card_id
    Args:
        card_id:
        status:
    """
    TrelloClient.move_trello_card(card_id, status)


def delete_item(card_id):
    """
    Deletes the item with the specified card_id
    Args:
        card_id:
    """
    TrelloClient.delete_trello_card(card_id)
