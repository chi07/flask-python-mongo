from internal.db.mongo_connector import Mongo


class RolePermissionRepository(object):
    __collection_name__ = "role_permissions"

    def __init__(self, mongo: Mongo, **kwargs) -> None:
        self.mongo = mongo
        self.__dict__.update(kwargs)

    def get(self, role_id: str, permission_id: str) -> dict:
        return self.mongo.database.role_permissions.find_one({"role_id": role_id, "permission_id": permission_id})

    def create(self, role_id: str, permission_id: str):
        return self.mongo.database.role_permissions.insert({"role_id": role_id, "permission_id": permission_id})

    def find(self, filter_condition=None):
        if filter_condition is None:
            return self.mongo.database.role_permissions.find({})
        return self.mongo.database.users.find(filter_condition)

    def delete(self, role_id: str, permission_id: str) -> None:
        if role_id is not None and permission_id is not None:
            return self.mongo.database.role_permissions.remove({"role_id": role_id, "permission_id": permission_id})
        else:
            raise Exception("Nothing to delete, because role_id parameter is None")
