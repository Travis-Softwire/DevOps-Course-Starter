from datetime import datetime

from todo_app.constants import NOT_STARTED
from todo_app.data.item import Item
from todo_app.data.todo_item_repository import TodoItemRepository
from todo_app.data.migration.trello_client import TrelloClient


def from_trello_card(card, trello_list):
    """
    Creates a new Item from a Trello card
    Args:
        card: the trello card
        trello_list: the list that the card belongs to

    Returns:
        a new Item object
    """
    display_date = None
    if card.get('due', None):
        display_date = datetime.fromisoformat(card['due']).strftime("%c")
    return Item(
        card['id'],
        card['name'],
        card['desc'],
        display_date,
        card['dateLastActivity'],
        trello_list['name']
    )


def items_from_trello_lists(trello_lists):
    """
    Creates a list of Items from a collection of trello lists
    Args:
        trello_lists: a collection of trello lists

    Returns:
        a list of Item objects
    """
    cards = []
    for trello_list in trello_lists:
        for card in trello_list.get('cards', []):
            cards.append(from_trello_card(card, trello_list))
    return cards


class TrelloItemRepository(TodoItemRepository):
    def get_items(self):
        trello_lists = TrelloClient.get_trello_lists()
        items = items_from_trello_lists(trello_lists)

        return sorted(items, key=Item.item_key)

    def add_item(self, title, description, due_date):
        TrelloClient.create_trello_card(title, description, due_date, NOT_STARTED)

    def update_status(self, card_id, status):
        TrelloClient.move_trello_card(card_id, status)

    def delete_item(self, card_id):
        TrelloClient.delete_trello_card(card_id)
