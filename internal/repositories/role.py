from bson.objectid import ObjectId

from internal.db.mongo_connector import Mongo
from internal.entities.role import Role


class RoleRepository(object):
    def __init__(self, mongo: Mongo, **kwargs) -> None:
        self.mongo = mongo
        self.__dict__.update(kwargs)

    def get(self, role_id: str):
        return self.mongo.database.roles.find_one({"_id": ObjectId(role_id)})

    def get_by_code(self, code: str) -> dict:
        return self.mongo.database.roles.find_one({"code": code})

    def create(self, role: Role):
        if role is not None:
            inserted_id = self.mongo.database.roles.insert(role.get_as_json())
            return self.get(inserted_id)
        else:
            raise Exception("Cannot save user into db because, user is None")

    def find(self, conditions: dict):
        if conditions is None:
            return self.mongo.database.users.find(conditions)
        return self.mongo.database.roles.find({})

    def update(self, role_id: str, data: dict) -> None:
        if role_id is not None:
            return self.mongo.database.roles.find_one_and_update(
                {"_id": ObjectId(role_id)},
                {"$set": data}, upsert=True
            )
        else:
            raise Exception("Nothing to update, because permission_id is None")

    def delete(self, role_id: str) -> None:
        return self.mongo.database.roles.remove({"_id": ObjectId(role_id)})
