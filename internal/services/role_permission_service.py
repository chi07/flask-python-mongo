from typing import Tuple

from internal.repositories.permission import PermissionRepository
from internal.repositories.role import RoleRepository
from internal.repositories.role_permission import RolePermissionRepository
from internal.repositories.user import UserRepository
from internal.repositories.user_permission import UserPermissionRepository


class RolePermissionService(object):
    def __init__(
            self,
            role_repo: RoleRepository,
            permission_repo: PermissionRepository,
            user_repo: UserRepository,
            user_permission_repo: UserPermissionRepository,
            role_permission_repo: RolePermissionRepository):
        self.role_repo = role_repo
        self.user_repo = user_repo
        self.permission_repo = permission_repo
        self.user_permission_repo = user_permission_repo
        self.role_permission_repo = role_permission_repo

    def add_role_permission(self, role_id: str, permission_id: str) -> Tuple[bool, str]:
        permission = self.permission_repo.get(permission_id)
        if not permission:
            return False, "can not found permission with id" + permission_id

        role = self.role_repo.get(role_id)
        if not role:
            return False, "can not found role with role id: " + role_id

        role_permission = self.get_permission(role_id, permission_id)
        if role_permission:
            return False, "The permission was granted to the role"

        return True, self.role_permission_repo.create(role_id, permission_id)

    def remove_role_permission(self, role_id: str, permission_id: str):
        return self.role_permission_repo.delete(role_id, permission_id)

    def get_permission(self, role_id: str, permission_id: str) -> dict:
        return self.role_permission_repo.get(role_id, permission_id)
