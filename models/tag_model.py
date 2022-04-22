from factory.validation import Validator
from factory.database import Database
from functions import convert_id


class Tag(object):
    def __init__(self):
        self.validator = Validator()
        self.db = Database()

        self.collection_name = 'tags'

        self.fields = {
            "name": "string",
            "used": "integer",
            "created": "datetime",
            "updated": "datetime",
        }

        self.create_required_fields = ["name", "used"]

        # Fields optional for CREATE
        self.create_optional_fields = []

        # Fields required for UPDATE
        self.update_required_fields = ["name", "used"]

        # Fields optional for UPDATE
        self.update_optional_fields = ["created", "updated"]

    def create(self, tag):
        # Validator will throw error if invalid
        self.validator.validate(
            tag, self.fields, self.create_required_fields, self.create_optional_fields)
        res = self.db.insert(tag, self.collection_name)
        return "Created tags : " + res

    def find(self, tag):  # find all
        return self.db.find(tag, self.collection_name)

    def get_10_favourites(self, tag):
        data = self.db.find(tag, self.collection_name,
                            raw=True).sort("used", -1).limit(10)
        data = convert_id(data)
        return data

    def update(self, id, tag):
        self.validator.validate(
            tag, self.fields, self.update_required_fields, self.update_optional_fields)
        return self.db.update(id, tag, self.collection_name)

    def delete(self, id):
        return self.db.delete(id, self.collection_name)
