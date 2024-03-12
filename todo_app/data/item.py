import datetime

from todo_app.constants import NOT_STARTED


class Item:
    def __init__(self, card_id, title, description, due_date, status=NOT_STARTED):
        self.id = card_id
        self.title = title
        self.description = description
        self.due_date = due_date
        self.status = status

    @classmethod
    def from_trello_card(cls, card, trello_list):
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
            display_date = datetime.datetime.fromisoformat(card['due']).strftime("%c")
        return cls(card['id'], card['name'], card['desc'], display_date, trello_list['name'])

    @classmethod
    def items_from_trello_lists(cls, trello_lists):
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
                cards.append(cls.from_trello_card(card, trello_list))
        return cards

