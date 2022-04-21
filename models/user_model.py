from factory.validation import Validator
from factory.database import Database


class User(object):
    def __init__(self):
        self.validator = Validator()
        self.db = Database()

        self.collection_name = 'users'

        self.fields = {
            "firstname": "string",
            "lastname": "string",
            "username": "string",
            "password": "string",
            "created": "datetime",
            "updated": "datetime",
        }

        self.create_required_fields = ["firstname", "lastname", "username", "password"]

        # Fields optional for CREATE
        self.create_optional_fields = []

        # Fields required for UPDATE
        self.update_required_fields = ["firstname", "lastname", "username", "password"]

        # Fields optional for UPDATE
        self.update_optional_fields = []

    def create(self, user):
        # Validator will throw error if invalid
        self.validator.validate(user, self.fields, self.create_required_fields, self.create_optional_fields)
        res = self.db.insert(user, self.collection_name)
        return "Created : " + res

    def find(self, filter):
        return self.db.find(filter, self.collection_name)

    def update(self, id, user):
        self.validator.validate(user, self.fields, self.update_required_fields, self.update_optional_fields)
        return self.db.update(id, user,self.collection_name)

    def delete(self, id):
        return self.db.delete(id, self.collection_name)
