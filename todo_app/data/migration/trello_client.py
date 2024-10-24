import os
import requests
from datetime import datetime

from todo_app.constants import NOT_STARTED, COMPLETED

TRELLO_KEY = os.environ.get('TRELLO_API_KEY', '')
TRELLO_TOKEN = os.environ.get('TRELLO_API_TOKEN', '')
TRELLO_TO_DO_BOARD_ID = os.environ.get('TRELLO_TO_DO_BOARD_ID', '')
TRELLO_ORGANIZATION_ID = os.environ.get('TRELLO_ORGANIZATION_ID')

CARDS_URL = f"https://api.trello.com/1/cards"
auth_params = {
    'key': TRELLO_KEY,
    'token': TRELLO_TOKEN,
}
card_request_params = {
    **auth_params,
    'cards': 'open',
    'card_fields': 'id,name,desc,due,dateLastActivity',
}
list_request_params = {
    'key': TRELLO_KEY,
    'token': TRELLO_TOKEN,
}


class TrelloClient:
    _list_ids = None

    @classmethod
    def get_trello_lists(cls):
        """
        Fetches the list of all lists available in the Trello
        Returns:
            The json response from the Trello API (the list of Trello lists if successful)
        """
        lists_url = f"https://api.trello.com/1/boards/{TRELLO_TO_DO_BOARD_ID}/lists"
        response = requests.get(lists_url, params=card_request_params)
        return response.json()

    @classmethod
    def _get_list_id(cls, list_name):
        """
        Utility function to get the id of the given list
        Args:
            list_name: the name of the list

        Returns:
            The id of the list
        """
        if cls._list_ids is None:
            cls._list_ids = {}
            for card_list in cls.get_trello_lists():
                cls._list_ids[card_list['name']] = card_list['id']
        return cls._list_ids[list_name]

    @classmethod
    def create_trello_card(cls, card_name, card_description, due_date, list_name):
        """
        Sends the POST request to create the new trello card
        Args:
            card_name: the name of the card you would like to create
            card_description: the description of the card you would like to create
            list_name: the name of the list to add the card to
            due_date: the date the task is due

        Returns:
            The json response from the Trello API (the created card if successful)
        """
        target_list_id = cls._get_list_id(list_name)
        create_card_params = {
            **card_request_params,
            'name': card_name,
            'desc': card_description,
            'due':  datetime.strptime(due_date, "%d/%m/%Y").isoformat(),
            'idList': target_list_id,
        }
        requests.post(CARDS_URL, params=create_card_params)

    @classmethod
    def move_trello_card(cls, card_id, to_list_name):
        """
        Sends a PUT request to change the status of the card
        Args:
            card_id: the id of the card you would like to move
            to_list_name: the name of the list to move the card to
        """
        target_list_id = cls._get_list_id(to_list_name)
        update_card_url = f"{CARDS_URL}/{card_id}"
        update_card_params = {
            **card_request_params,
            'idList': target_list_id,
        }
        requests.put(update_card_url, params=update_card_params)

    @classmethod
    def delete_trello_card(cls, card_id):
        """
        Sends a DELETE request to remove the card
        Args:
            card_id: the id of the card you would like to delete
        """
        delete_card_url = f"{CARDS_URL}/{card_id}"
        requests.delete(delete_card_url, params=card_request_params)

    @classmethod
    def create_list(cls, board_id, list_name):
        """
        Sends a POST request to create a new list on a board
        Args:
            board_id: id of the board to add a list to
            list_name: name of the list to add
        """
        create_list_url = f"https://api.trello.com/1/boards/{board_id}/lists"
        create_list_params = {
            **auth_params,
            'name': list_name,
        }
        requests.post(create_list_url, params=create_list_params)

    @classmethod
    def create_board(cls, board_name):
        """
        Sends a POST request to create a new board
        Args:
            board_name: the name of the new board

        Returns:
            board_id: the id of the created board
        """
        create_board_url = "https://api.trello.com/1/boards/"
        create_board_params = {
            **auth_params,
            'name': board_name,
            'idOrganization': TRELLO_ORGANIZATION_ID,
            'defaultLists': 'false',
        }
        response = requests.post(create_board_url, params=create_board_params)
        board_id = response.json().get("id")
        for list_name in [NOT_STARTED, COMPLETED]:
            cls.create_list(board_id, list_name)
        return board_id


    @classmethod
    def delete_board(cls, board_id):
        """
        Sends a DELETE request to remove the board
        Args:
            board_id: id of the board you would like to delete
        """
        delete_board_url = f"https://api.trello.com/1/boards/{board_id}/"
        requests.delete(delete_board_url, params=auth_params)


