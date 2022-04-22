from datetime import datetime
from pymongo import MongoClient
from bson import ObjectId

from config import config
from functions import convert_id


class Database(object):
    def __init__(self):
        self.client = MongoClient(config['db']['url'])  # configure db url
        self.db = self.client[config['db']['name']]  # configure db name

    def insert(self, element, collection_name):
        element["created"] = datetime.now()
        element["updated"] = datetime.now()
        inserted = self.db[collection_name].insert_one(
            element)  # insert data to db
        return str(inserted.inserted_id)

    def find(self, criteria, collection_name, projection=None, sort=None, limit=0, skip=0, raw=False):  # find all from db

        if "_id" in criteria:
            criteria["_id"] = ObjectId(criteria["_id"])

        found = self.db[collection_name].find(
            filter=criteria, projection=projection, skip=skip, limit=limit, sort=sort)

        if raw:
            return found

        found = convert_id(found)
        return found

    def find_by_id(self, id, collection_name):
        found = self.db[collection_name].find_one({"_id": ObjectId(id)})

        if found is None:
            return not found

        if "_id" in found:
            found["_id"] = str(found["_id"])

        return found

    def update(self, id, element, collection_name):
        criteria = {"_id": ObjectId(id)}

        element["updated"] = datetime.now()
        set_obj = {"$set": element}  # update value

        updated = self.db[collection_name].update_one(criteria, set_obj)
        if updated.matched_count == 1:
            return "Record Successfully Updated"

    def delete(self, id, collection_name):
        deleted = self.db[collection_name].delete_one({"_id": ObjectId(id)})
        return bool(deleted.deleted_count)
