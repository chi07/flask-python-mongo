from flask import Blueprint
from flask_restful import Api

from internal.db.mongo_connector import Mongo
from internal.http.handlers.health_check import HealthCheckHandler
from internal.http.handlers.login import LoginHandler
from internal.http.handlers.permission_add import AddPermissionHandler
from internal.http.handlers.permission_check import CheckPermissionHandler
from internal.http.handlers.permission_delete import DeletePermissionHandler
from internal.http.handlers.permission_edit import EditPermissionHandler
from internal.http.handlers.permission_list import ListPermissionHandler
from internal.http.handlers.role_add import AddRoleHandler
from internal.http.handlers.role_delete import DeleteRoleHandler
from internal.http.handlers.role_edit import EditRoleHandler
from internal.http.handlers.role_list import ListRoleHandler
from internal.http.handlers.role_permissions import AddRolePermissionHandler
from internal.http.handlers.role_permissions_delete import \
    DeleteRolePermissionHandler
from internal.http.handlers.user_handler import AddUserHandler
from internal.http.handlers.user_list_handler import ListUserHandler
from internal.http.handlers.user_permissions import AddUserPermissionHandler
from internal.http.handlers.user_permissions_delete import \
    RemoveUserPermissionHandler
from internal.http.handlers.workspace_add import AddWorkspaceHandler
from internal.http.handlers.workspace_detail import ShowWorkspaceHandler
from internal.http.handlers.workspace_edit import EditWorkspaceHandler
from internal.http.handlers.workspace_list import ListWorkspaceHandler
from internal.repositories.permission import PermissionRepository
from internal.repositories.role import RoleRepository
from internal.repositories.role_permission import RolePermissionRepository
from internal.repositories.user import UserRepository
from internal.repositories.user_permission import UserPermissionRepository
from internal.repositories.workspace import WorkspaceRepository
from internal.services.auth import AuthService
from internal.services.check_permission_service import CheckPermissionService
from internal.services.permission_service import PermissionService
from internal.services.role_permission_service import RolePermissionService
from internal.services.role_service import RoleService
from internal.services.user_permission_service import UserPermissionService
from internal.services.user_service import UserService
from internal.services.workspace_service import WorkspaceService

db = Mongo.get_instance()
role_repo = RoleRepository(db)
user_repo = UserRepository(db)
workspace_repo = WorkspaceRepository(db)
user_service = UserService(user_repo, role_repo, workspace_repo)
role_service = RoleService(role_repo)
permission_repo = PermissionRepository(db)
permission_service = PermissionService(permission_repo)
workspace_service = WorkspaceService(workspace_repo)
role_permission_repo = RolePermissionRepository(db)
user_permission_repo = UserPermissionRepository(db)
role_permission_service = RolePermissionService(role_repo, permission_repo, user_repo, user_permission_repo,
                                                role_permission_repo)

user_permission_service = UserPermissionService(user_repo, role_repo, permission_repo, user_permission_repo,
                                                role_permission_repo)

auth_service = AuthService(user_repo)
check_permission_service = CheckPermissionService(role_repo, permission_repo, user_permission_repo,
                                                  role_permission_repo)

bp = Blueprint("api", __name__)
api = Api(bp)

api.add_resource(HealthCheckHandler, "/")
api.add_resource(LoginHandler, "/login", resource_class_kwargs={'service': auth_service})
api.add_resource(ListUserHandler, "/users", resource_class_kwargs={'service': user_service})
api.add_resource(AddUserHandler, "/users/add", resource_class_kwargs={'service': user_service})

api.add_resource(ListRoleHandler, "/roles", resource_class_kwargs={'service': role_service})
api.add_resource(AddRoleHandler, "/roles/add", resource_class_kwargs={'service': role_service})
api.add_resource(EditRoleHandler, "/roles/<role_id>", resource_class_kwargs={'service': role_service})
api.add_resource(DeleteRoleHandler, "/roles/<role_id>", resource_class_kwargs={'service': role_service})

api.add_resource(ListPermissionHandler, "/permissions", resource_class_kwargs={'service': permission_service})
api.add_resource(AddPermissionHandler, "/permissions/add", resource_class_kwargs={'service': permission_service})
api.add_resource(EditPermissionHandler, "/permissions/<permission_id>",
                 resource_class_kwargs={'service': permission_service})
api.add_resource(DeletePermissionHandler, "/permissions/<permission_id>",
                 resource_class_kwargs={'service': permission_service})

api.add_resource(AddUserPermissionHandler, "/permissions/users/add",
                 resource_class_kwargs={'service': user_permission_service})
api.add_resource(RemoveUserPermissionHandler, "/permissions/users/delete",
                 resource_class_kwargs={'service': user_permission_service})
api.add_resource(AddRolePermissionHandler, "/permissions/roles/add",
                 resource_class_kwargs={'service': role_permission_service})

api.add_resource(DeleteRolePermissionHandler, "/permissions/roles/delete",
                 resource_class_kwargs={'service': role_permission_service})

api.add_resource(ListWorkspaceHandler, "/workspaces", resource_class_kwargs={'service': workspace_service})
api.add_resource(AddWorkspaceHandler, "/workspaces/add", resource_class_kwargs={'service': workspace_service})
api.add_resource(EditWorkspaceHandler, "/workspaces/<workspace_id>",
                 resource_class_kwargs={'service': workspace_service})
api.add_resource(ShowWorkspaceHandler, "/workspaces/<workspace_id>",
                 resource_class_kwargs={'service': workspace_service})

api.add_resource(CheckPermissionHandler, "/permissions/check",
                 resource_class_kwargs={'service': check_permission_service})
