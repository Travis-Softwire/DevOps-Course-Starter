from todo_app.data.cosmos_client import CosmosClient
from todo_app.data.todo_item_repository import TodoItemRepository


class CosmosItemRepository(TodoItemRepository):
    def __init__(self):
        self.cosmos_client = CosmosClient()

    def get_items(self):
        return self.cosmos_client.list_items()

    def add_item(self, title, description, due_date):
        return self.cosmos_client.create_item(title=title, description=description, due_date=due_date)

    def update_status(self, item_id, status):
        self.cosmos_client.update_item(item_id=item_id, status=status)

    def delete_item(self, item_id):
        self.cosmos_client.delete_item(item_id)
