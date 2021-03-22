from typing import Tuple

from internal.repositories.permission import PermissionRepository
from internal.repositories.role import RoleRepository
from internal.repositories.role_permission import RolePermissionRepository
from internal.repositories.user import UserRepository
from internal.repositories.user_permission import UserPermissionRepository


class UserPermissionService(object):
    def __init__(
            self,
            user_repo: UserRepository,
            role_repo: RoleRepository,
            permission_repo: PermissionRepository,
            user_permission_repo: UserPermissionRepository,
            role_permission_repo: RolePermissionRepository):
        self.role_repo = role_repo
        self.user_repo = user_repo
        self.permission_repo = permission_repo
        self.user_permission_repo = user_permission_repo
        self.role_permission_repo = role_permission_repo

    def add_user_permission(self, user_id: str, permission_id: str, attributes=None) -> Tuple[bool, str]:
        if attributes is None:
            attributes = ['*']

        permission = self.permission_repo.get(permission_id)
        if not permission:
            return False, "can not found permission with your request id"

        existed_permission = self.get_permission(user_id, permission_id)
        if existed_permission:
            return False, "The role name was taken. Please set other role"

        return True, self.user_permission_repo.create(user_id, permission_id, attributes)

    def remove_user_permission(self, user_id: str, permission_id: str) -> Tuple[bool, str]:
        permission = self.permission_repo.get(permission_id)

        if not permission:
            return False, "permission not found with id: " + permission_id

        user_permission = self.get_permission(user_id, permission_id)
        if not user_permission:
            return False, "This user does not has permission with id: " + permission_id
        self.user_permission_repo.delete(user_id, permission_id)

        return True, "success"

    def get_permission(self, user_id: str, permission_id: str) -> dict:
        return self.user_permission_repo.get_user_permission(user_id, permission_id)
