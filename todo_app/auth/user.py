from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, user_id, name, roles=[]):
        self.id = str(user_id)
        self.name = name
        self.roles = roles
