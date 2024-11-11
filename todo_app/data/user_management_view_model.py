import functools

from flask_login import current_user


class UserManagementViewModel:
    def __init__(self, users):
        self._users = users

    @property
    def users(self):
        return [user for user in self._users if user.id != current_user.get_id()]
