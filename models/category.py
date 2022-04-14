from factory.validation import Validator
from factory.database import Database


class Category(object):
    def __init__(self):
        self.validator = Validator()
        self.db = Database()

        self.collection_name = 'categories'

        self.fields = {
            "name": "string",
            "created": "datetime",
            "updated": "datetime",
        }

        self.create_required_fields = ["name"]

        # Fields optional for CREATE
        self.create_optional_fields = []

        # Fields required for UPDATE
        self.update_required_fields = ["name"]

        # Fields optional for UPDATE
        self.update_optional_fields = []

    def create(self, category):
        # Validator will throw error if invalid
        self.validator.validate(
            category, self.fields, self.create_required_fields, self.create_optional_fields)
        category["_id"] = category["name"]
        res = self.db.insert(category, self.collection_name)
        return "Created category : " + res

    def find(self, category):  # find all
        return self.db.find(category, self.collection_name)

    def update(self, id, category):
        self.validator.validate(
            category, self.fields, self.update_required_fields, self.update_optional_fields)
        return self.db.update(id, category, self.collection_name)

    def delete(self, id):
        return self.db.delete(id, self.collection_name)
