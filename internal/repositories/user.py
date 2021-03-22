from bson.objectid import ObjectId

from internal.db.mongo_connector import Mongo
from internal.entities.user import User


def add_user():
    return 1


class UserRepository(object):
    __collection_name__ = "users"

    def __init__(self, mongo: Mongo, **kwargs) -> None:
        self.mongo = mongo
        self.__dict__.update(kwargs)

    def get(self, user_id: str) -> dict:
        return self.mongo.database.users.find_one({"_id": ObjectId(user_id)})

    def get_by_email(self, email: str) -> User:
        return self.mongo.database.users.find_one({"email": email})

    def get_by_username(self, username: str) -> User:
        return self.mongo.database.users.find_one({"username": username})

    def create(self, user: User):
        if user is not None:
            inserted_id = self.mongo.database.users.insert(user.get_as_json())
            return self.get(inserted_id)
        else:
            raise Exception("Cannot save user into db because, user is None")

    def find(self, filter_condition=None):
        if filter_condition is None:
            return self.mongo.database.users.find({})
        return self.mongo.database.users.find(filter_condition)

    def update(self, user: User) -> None:
        if user is not None:
            self.mongo.database.users.save(user.get_as_json())
        else:
            raise Exception("Nothing to update, because user parameter is None")

    def delete(self, user: User) -> None:
        if user is not None:
            self.mongo.database.users.remove(user.get_as_json())
        else:
            raise Exception("Nothing to delete, because user parameter is None")
