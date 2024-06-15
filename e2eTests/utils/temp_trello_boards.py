from todo_app.data.trello_client import TrelloClient


def create_trello_board(name):
    return TrelloClient.create_board(name)


def delete_trello_board(board_id):
    return TrelloClient.delete_board(board_id)
