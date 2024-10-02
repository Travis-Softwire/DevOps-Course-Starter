from abc import ABC, abstractmethod

class TodoItemRepository(ABC):
    @abstractmethod
    def get_items(self):
        """
        Fetches all saved items from store.

        Returns:
            list: a sorted list of saved items.
        """
        raise NotImplementedError

    @abstractmethod
    def add_item(self, title, description, due_date):
        """
        Adds a new saved item.

        Args:
            title: the title of the item.
            description: Item description.
            due_date: Item due date.
        """
        raise NotImplementedError

    @abstractmethod
    def update_status(self, item_id, status):
        """
        Updates the status of a saved item.

        Args:
            item_id: The item id.
            status: The new status.
        """
        raise NotImplementedError

    @abstractmethod
    def delete_item(self, item_id):
        """
        Deletes a saved item.

        Args:
            item_id: Item id.
        """
        raise NotImplementedError

