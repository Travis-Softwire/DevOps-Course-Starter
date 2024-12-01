import os
from datetime import datetime, timezone

import pymongo
from bson.objectid import ObjectId

from todo_app.constants import NOT_STARTED
from todo_app.data.item import Item

COSMOS_CONNECTION_STRING = os.environ.get('COSMOS_CONNECTION_STRING')


def todo_from_cosmos_item(cosmos_item):
    todo = cosmos_item.copy()
    object_id = todo.pop('_id')
    todo['item_id'] = str(object_id)
    return Item(**todo)


class CosmosClient:
    def __init__(self):
        internal_client = pymongo.MongoClient(COSMOS_CONNECTION_STRING)
        db = internal_client.todoapp_db
        self.collection = db.todos

    def list_items(self):
        return list(map(todo_from_cosmos_item, list(self.collection.find({}))))

    def create_item(self, title, description, due_date):
        return self.collection.insert_one({
            'title': title,
            'description': description,
            'due_date': due_date,
            'last_modified': datetime.now(timezone.utc).isoformat(),
            'status': NOT_STARTED
        })

    def update_item(self, item_id, status):
        self.collection.update_one({'_id': ObjectId(item_id)}, {'$set': {'status': status, 'last_modified': datetime.now(timezone.utc).isoformat()}})

    def delete_item(self, item_id):
        self.collection.delete_one({'_id': ObjectId(item_id)})
