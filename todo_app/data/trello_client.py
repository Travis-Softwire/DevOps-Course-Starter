import os
import requests

TRELLO_KEY = os.environ.get('TRELLO_API_KEY', '')
TRELLO_TOKEN = os.environ.get('TRELLO_API_TOKEN', '')
TRELLO_TO_DO_BOARD_ID = os.environ.get('TRELLO_TO_DO_BOARD_ID', '')

LISTS_URL = f"https://api.trello.com/1/boards/{TRELLO_TO_DO_BOARD_ID}/lists"
CARDS_URL = f"https://api.trello.com/1/cards"
card_request_params = {
    'key': TRELLO_KEY,
    'token': TRELLO_TOKEN,
    'cards': 'open',
    'card_fields': 'id,name,desc,due',
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
        return requests.get(LISTS_URL, params=card_request_params).json()

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

        Returns:
            The json response from the Trello API (the created card if successful)
        """
        target_list_id = cls._get_list_id(list_name)
        create_card_params = {
            **card_request_params,
            'name': card_name,
            'desc': card_description,
            'due': due_date,
            'idList': target_list_id,
        }
        requests.post(CARDS_URL, params=create_card_params).json().get('id', None)

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

