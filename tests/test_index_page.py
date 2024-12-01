import importlib
import os
from datetime import datetime, timezone

import mongomock
import pymongo
import pytest
from dotenv import find_dotenv, load_dotenv
import todo_app.data.cosmos_client
from todo_app import create_app

from todo_app.constants import NOT_STARTED


@pytest.fixture
def client():
    # Use our test integration config instead of the 'real' version
    file_path = find_dotenv('./.env.test')
    load_dotenv(file_path, override=True)
    importlib.reload(todo_app.data.cosmos_client)

    with mongomock.patch(servers=(('fakemongo.com', 27017),)):
        # Create the new app.
        test_app = create_app()

        # Use the app to create a test_client that can be used in our tests.
        with test_app.test_client() as client:
            yield client


def test_index_page(monkeypatch, client):
    # Arrange
    pymongo.MongoClient(os.environ.get('COSMOS_CONNECTION_STRING')).todoapp_db.todos.insert_one({
        'title': "Test card",
        'description': "test desc",
        'due_date': "01/01/01",
        'last_modified': datetime.now(timezone.utc).isoformat(),
        'status': NOT_STARTED
    })

    # Act
    response = client.get('/')

    # Assert
    assert response.status_code == 200
    assert 'Test card' in response.data.decode()
