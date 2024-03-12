from datetime import datetime

from todo_app.constants import COMPLETED, NOT_STARTED, SHOW_ALL_DONE_ITEMS_THRESHOLD


class ViewModel:
    def __init__(self, items):
        self._items = items

    @property
    def items(self):
        if self.should_show_all_done_items:
            return [*self.not_started_items, *self.done_items]
        else:
            return [*self.not_started_items, *self.recent_done_items]

    @property
    def done_items(self):
        return [item for item in self._items if item.status == COMPLETED]

    @property
    def recent_done_items(self):
        return [
            item for item in self.done_items
            if datetime.fromisoformat(item.last_modified).date() == datetime.today().date()
        ]

    @property
    def older_done_items(self):
        return [
            item for item in self.done_items
            if datetime.fromisoformat(item.last_modified).date() != datetime.now().date()
        ]

    @property
    def not_started_items(self):
        return [item for item in self._items if item.status == NOT_STARTED]

    @property
    def should_show_all_done_items(self):
        return (len(self.done_items) <= SHOW_ALL_DONE_ITEMS_THRESHOLD
                or len(self.older_done_items) == 0)
