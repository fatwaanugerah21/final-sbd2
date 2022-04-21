from factory.validation import Validator
from factory.database import Database
from config import config
from functions import convert_id


class News(object):
    def __init__(self):
        self.validator = Validator()
        self.db = Database()

        self.collection_name = 'news'

        self.fields = {
            "title": "string",
            "writer": "string",
            "text": "string",
            "category": "string",
            "tags": "array",
            "readed": "integer",
            "created": "datetime",
            "updated": "datetime",
        }

        self.create_required_fields = [
            "title", "writer", "text", "category", "readed", "tags"]

        # Fields optional for CREATE
        self.create_optional_fields = []

        # Fields required for UPDATE
        self.update_required_fields = [
            "title", "writer", "text", "category", "readed", "tags"]

        # Fields optional for UPDATE
        self.update_optional_fields = ["created", "updated"]

    def create(self, news):
        # Validator will throw error if invalid
        self.validator.validate(
            news, self.fields, self.create_required_fields, self.create_optional_fields)
        res = self.db.insert(news, self.collection_name)
        return "Inserted Id " + res

    def find(self, filter, start, sort=["created", -1], limit=config["news_limit"]):
        # skip & limit is for pagination
        # limit + 1 is for checking hasMore
        data = self.db.find(filter, self.collection_name,
                            cursor=True).skip(start).limit(limit).sort(sort[0], sort[1])
        data = convert_id(data)

        # Pagination stuff
        count = len(data)
        nextData = self.db.find(
            filter, self.collection_name, skip=start + limit, limit=1)
        hasMore = len(nextData) >= 1
        pagination = {
            "count": count,
            "hasMore": hasMore
        }

        return {"data": data, "pagination": pagination}

    def find_by_id(self, id):
        return self.db.find_by_id(id, self.collection_name)

    def update(self, id, news):
        self.validator.validate(
            news, self.fields, self.update_required_fields, self.update_optional_fields)
        return self.db.update(id, news, self.collection_name)

    def delete(self, id):
        return self.db.delete(id, self.collection_name)
