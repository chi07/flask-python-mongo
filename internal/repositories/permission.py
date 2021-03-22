from bson.objectid import ObjectId

from internal.db.mongo_connector import Mongo
from internal.entities.permission import Permission


class PermissionRepository(object):
    def __init__(self, mongo: Mongo, **kwargs) -> None:
        self.mongo = mongo
        self.__dict__.update(kwargs)

    def get(self, permission_id: str):
        return self.mongo.database.permissions.find_one({"_id": ObjectId(permission_id)})

    def get_by_resource(self, resource: str) -> dict:
        return self.mongo.database.permissions.find_one({"resource": resource})

    def get_by_name(self, name: str) -> dict:
        return self.mongo.database.permissions.find_one({"name": name})

    def create(self, permission: Permission):
        if permission is not None:
            inserted_id = self.mongo.database.permissions.insert(permission.get_as_json())
            return self.get(inserted_id)
        else:
            raise Exception("Cannot save user into db because, user is None")

    def find(self, conditions: dict):
        if conditions is None:
            return self.mongo.database.permissions.find(conditions)
        return self.mongo.database.permissions.find({})

    def update(self, permission_id: str, data: dict) -> None:
        if permission_id is not None:
            return self.mongo.database.permissions.find_one_and_update(
                {"_id": ObjectId(permission_id)},
                {"$set": data}, upsert=True
            )
        else:
            raise Exception("Nothing to update, because permission_id is None")

    def delete(self, permission_id: str) -> None:
        return self.mongo.database.permissions.remove({"_id": ObjectId(permission_id)})
