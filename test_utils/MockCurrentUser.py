import importlib
import os
import flask_login

import todo_app


class MockCurrentUser:
    default_user_id = 1234

    def __init__(self, user_id=default_user_id):
        self._user_id = user_id

    @classmethod
    def setup_mock_user(cls, monkeypatch, pymongo):
        pymongo.MongoClient(os.environ.get('COSMOS_CONNECTION_STRING')).todoapp_db.users.insert_one({
            'user_id': cls.default_user_id,
            'name': "test admin",
            'due_date': "01/01/01",
            'roles': ['Admin', 'Reader']
        })

        mock_current_user = cls()
        monkeypatch.setattr(flask_login, "current_user", mock_current_user)
        importlib.reload(todo_app.auth.current_todo_user)

    @classmethod
    def delete_mock_user(cls, pymongo, user_id=default_user_id):
        pymongo.MongoClient(os.environ.get('COSMOS_CONNECTION_STRING')).todoapp_db.users.delete_one({
            'user_id': user_id
        })

    def get_id(self):
        return self._user_id
