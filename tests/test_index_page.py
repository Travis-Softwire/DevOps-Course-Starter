import importlib
import os
import pytest
import requests
from dotenv import find_dotenv, load_dotenv
import todo_app.data.trello_client
from todo_app import create_app

@pytest.fixture
def client():
    # Use our test integration config instead of the 'real' version
    # Create the new app.
    file_path = find_dotenv('./.env.test')
    load_dotenv(file_path, override=True)
    importlib.reload(todo_app.data.trello_client)

    test_app = create_app()

    # Use the app to create a test_client that can be used in our tests.
    with test_app.test_client() as client:
        yield client


def test_index_page(monkeypatch, client):
    # Arrange
    monkeypatch.setattr(requests, 'get', stub)

    # Act
    response = client.get('/')

    # Assert
    assert response.status_code == 200
    assert 'Test card' in response.data.decode()


class StubResponse():
    def __init__(self, fake_response_data):
        self.fake_response_data = fake_response_data

    def json(self):
        return self.fake_response_data


def stub(url, params={}):
    test_board_id = os.environ.get('TRELLO_TO_DO_BOARD_ID')
    if url == f"https://api.trello.com/1/boards/{test_board_id}/lists":
        fake_response_data = [{
            'id': '123abc',
            'name': 'Not Started',
            'cards': [
                {
                    'id': '456',
                    'name': 'Test card',
                    'desc': 'Test description',
                    'due': '2030-01-01T00:00:00Z',
                    'dateLastActivity': '2024-01-01T00:00:00Z',
                }
            ]
        }]
        return StubResponse(fake_response_data)

    raise Exception(f'Integration test did not expect URL "{url}"')