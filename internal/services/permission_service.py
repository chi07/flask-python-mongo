from datetime import datetime
from typing import Tuple, Type

from internal.entities.permission import PERMISSION_STATUS_ACTIVE, Permission
from internal.repositories.permission import PermissionRepository


class PermissionService(object):
    def __init__(self, permission_repo: PermissionRepository):
        self.permission_repo = permission_repo

    def add_permission(self, p: Permission) -> Tuple[bool, Type[Permission], str]:
        permission = self.get_by_resource(p.name)
        if permission:
            return False, Permission, "The permission name was taken. Please set other permission"

        now = datetime.now()
        p.createdAt = now
        p.updatedAt = now
        p.status = PERMISSION_STATUS_ACTIVE

        return True, self.permission_repo.create(p), "Created new permission successfully"

    def update_permission(self, permission_id: str, data: dict):
        return self.permission_repo.update(permission_id, data)

    def delete_permission(self, permission_id: str):
        return self.permission_repo.delete(permission_id)

    def get_by_resource(self, resource: str) -> dict:
        return self.permission_repo.get_by_resource(resource)

    def get_by_id(self, permission_id: str) -> dict:
        return self.permission_repo.get(permission_id)

    def get_all(self) -> dict:
        return self.permission_repo.find({})
