from flask import session

from internal.entities.role import (ROLE_TYPE_SYS_ADMIN,
                                    ROLE_TYPE_WORKSPACE_ADMIN)
from internal.repositories.permission import PermissionRepository
from internal.repositories.role import RoleRepository
from internal.repositories.role_permission import RolePermissionRepository
from internal.repositories.user_permission import UserPermissionRepository


class CheckPermissionService(object):
    def __init__(
            self,
            role_repo: RoleRepository,
            permission_repo: PermissionRepository,
            user_permission_repo: UserPermissionRepository,
            role_permission_repo: RolePermissionRepository):
        self.role_repo = role_repo
        self.permission_repo = permission_repo
        self.user_permission_repo = user_permission_repo
        self.role_permission_repo = role_permission_repo

    def check_user_permission(self, name):
        user = session['current_user']
        role_id = user['roleID']
        user_type = user['userType']

        if user_type == ROLE_TYPE_SYS_ADMIN or user_type == ROLE_TYPE_WORKSPACE_ADMIN:
            return True, 'permission granted', ['*']

        permission = self.permission_repo.get_by_name(name)
        if not permission:
            return False, 'does not have permission', []

        permission_id = str(permission['_id'])
        user_permission = self.user_permission_repo.get_user_permission(user['id'], permission_id)
        if user_permission:
            return True, user_permission['attributes'], []

        if role_id is None:
            return False, 'user does not belong any group', []
        role_permission = self.role_permission_repo.get(role_id, permission_id)
        if role_permission:
            return True, 'permission granted', []

        return False, 'does not have permission', []
