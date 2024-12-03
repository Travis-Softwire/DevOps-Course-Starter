from todo_app.auth.user import User
from todo_app.data.cosmos_client import CosmosClient
from todo_app.data.user_repository import UserRepository


class CosmosUserRepository(UserRepository):
    def __init__(self):
        self.cosmos_client = CosmosClient()

    def get_user_from_id(self, user_id):
        cosmos_user = self.cosmos_client.lookup_user(user_id)
        if cosmos_user is None:
            return None
        else:
            return User(cosmos_user['user_id'], cosmos_user['name'], cosmos_user['roles'])

    def get_users(self):
        users = self.cosmos_client.list_users()
        return list(map(lambda cosmos_user: User(cosmos_user['user_id'], cosmos_user['name'], cosmos_user['roles']), users))

    def save_user(self, user):
        self.cosmos_client.create_user_if_new(user)

    def delete_user(self, user_id):
        self.cosmos_client.delete_user(user_id)

    def set_user_roles(self, user_id, roles):
        self.cosmos_client.set_user_roles(user_id, roles)

    def add_user_role(self, user_id, role):
        user = self.get_user_from_id(user_id)
        roles = user.roles
        if role not in roles:
            roles.append(role)
            self.set_user_roles(user_id, roles)

    def remove_user_role(self, user_id, role):
        user = self.get_user_from_id(user_id)
        roles = user.roles
        if role in roles:
            roles.remove(role)
            self.set_user_roles(user_id, roles)

    def does_user_have_role(self, user_id, role):
        return self.cosmos_client.user_has_role(user_id, role)
