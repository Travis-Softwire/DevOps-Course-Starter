import datetime

from todo_app.constants import NOT_STARTED


class Item:
    def __init__(self, item_id, title, description, due_date, last_modified, status=NOT_STARTED):
        self.id = item_id
        self.title = title
        self.description = description
        self.due_date = due_date
        self.last_modified = last_modified
        self.status = status

    @classmethod
    def item_key(cls, item):
        return item.status
