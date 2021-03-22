from internal.db.mongo_connector import Mongo


class UserPermissionRepository(object):
    __collection_name__ = "user_permissions"

    def __init__(self, mongo: Mongo, **kwargs) -> None:
        self.mongo = mongo
        self.__dict__.update(kwargs)

    def get_user_permission(self, user_id: str, permission_id: str) -> dict:
        return self.mongo.database.user_permissions.find_one({"user_id": user_id, "permission_id": permission_id})

    def create(self, user_id: str, permission_id: str, attributes=None):
        return self.mongo.database.user_permissions.insert(
            {"user_id": user_id, "permission_id": permission_id, "attributes": attributes})

    def find(self, filter_condition=None):
        if filter_condition is None:
            return self.mongo.database.user_permissions.find({})
        return self.mongo.database.users.find(filter_condition)

    def delete(self, user_id: str, permission_id: str) -> None:
        if user_id is not None and permission_id is not None:
            return self.mongo.database.user_permissions.remove({"user_id": user_id, "permission_id": permission_id})
        else:
            raise Exception("Nothing to delete, because user_id and permission_id parameter is None")
