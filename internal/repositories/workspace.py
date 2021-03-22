from bson.objectid import ObjectId

from internal.db.mongo_connector import Mongo
from internal.entities.workspace import Workspace


class WorkspaceRepository(object):
    def __init__(self, mongo: Mongo, **kwargs) -> None:
        self.mongo = mongo
        self.__dict__.update(kwargs)

    def get(self, workspace_id: str):
        return self.mongo.database.workspaces.find_one({"_id": ObjectId(workspace_id)})

    def get_by_name(self, name: str) -> dict:
        return self.mongo.database.workspaces.find_one({"name": name})

    def create(self, workspace: Workspace):
        if workspace is not None:
            inserted_id = self.mongo.database.workspaces.insert(workspace.get_as_json())
            return self.get(inserted_id)
        else:
            raise Exception("Cannot save user into db because, user is None")

    def find(self, conditions: None):
        if conditions is None:
            return self.mongo.database.users.find(conditions)
        return self.mongo.database.workspaces.find({})

    def update(self, workspace_id: str, data: dict) -> None:
        if workspace_id is not None:
            return self.mongo.database.workspaces.find_one_and_update(
                {"_id": ObjectId(workspace_id)},
                {"$set": data}, upsert=True
            )
        else:
            raise Exception("Nothing to update, because permission_id is None")

    def delete(self, workspace_id: str) -> None:
        return self.mongo.database.workspaces.remove({"_id": ObjectId(workspace_id)})
