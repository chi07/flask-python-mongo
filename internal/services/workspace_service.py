from datetime import datetime
from typing import Tuple, Type

from internal.entities.workspace import WORKSPACE_STATUS_ACTIVE, Workspace
from internal.repositories.workspace import WorkspaceRepository


class WorkspaceService(object):
    def __init__(self, workspace_repo: WorkspaceRepository):
        self.workspace_repo = workspace_repo

    def add_workspace(self, workspace: Workspace) -> Tuple[bool, Type[Workspace], str]:
        existed_workspace = self.workspace_repo.get_by_name(workspace.name)
        if existed_workspace:
            return False, Workspace, "The workspace name was taken"

        now = datetime.now()
        workspace.createdAt = now
        workspace.updatedAt = now
        workspace.status = WORKSPACE_STATUS_ACTIVE

        return True, self.workspace_repo.create(workspace), "Created new workspace successfully"

    def update_workspace(self, workspace_id: str, data):
        return self.workspace_repo.update(workspace_id, data)

    def delete_workspace(self, workspace_id: str):
        return self.workspace_repo.delete(workspace_id)

    def get_by_name(self, name: str) -> dict:
        return self.workspace_repo.get_by_name(name)

    def get_by_id(self, workspace_id: str) -> dict:
        return self.workspace_repo.get(workspace_id)

    def get_all(self) -> dict:
        return self.workspace_repo.find({})
