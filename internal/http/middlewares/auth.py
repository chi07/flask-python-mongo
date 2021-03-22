"""Authentication utilities needed by API."""

from functools import wraps

from flask import request
from werkzeug.exceptions import Forbidden, Unauthorized

from internal.db.mongo_connector import Mongo
from internal.entities.user import User
from internal.repositories.permission import PermissionRepository
from internal.repositories.role import RoleRepository
from internal.repositories.role_permission import RolePermissionRepository
from internal.repositories.user import UserRepository
from internal.repositories.user_permission import UserPermissionRepository
from internal.services.auth import AuthService
from internal.services.permission_service import PermissionService
from internal.services.role_permission_service import RolePermissionService
from internal.services.role_service import RoleService
from internal.services.user_permission_service import UserPermissionService


def __check_permission(name: str, user: User):
    role_repo = RoleRepository(Mongo.get_instance())
    role_service = RoleService(role_repo)
    permission_repo = PermissionRepository(Mongo.get_instance())
    permission_service = PermissionService(permission_repo)
    role_permission_repo = RolePermissionRepository(Mongo.get_instance())
    role_permission_service = RolePermissionService(role_permission_repo)
    user_permission_repo = UserPermissionRepository(Mongo.get_instance())
    user_permission_service = UserPermissionService(user_permission_repo)

    permission = permission_service.get_by_resource(name)
    if not permission:
        return False, []

    permission_id = str(permission['_id'])
    user_permission = user_permission_service.get_permission(user.id, permission_id)
    if user_permission:
        return True, user_permission['attributes']

    role_id = user.roleID
    role_permission = role_permission_service.get_permission(role_id, permission_id)
    if role_permission:
        return True, []


def get_access_token():
    access_token: str
    try:
        access_token = request.headers.get('Authorization')
    except KeyError:
        return {"message": "Authentication token is missing."}, Unauthorized.code

    return access_token


def auth(f):
    """
    Perform token based authentication.
    Token is supposed to be passed in headers.
    If found, decrypt token and get matching user.
    If no token in header or user not found, return an error message.
    """

    @wraps(f)
    def decorated(*args, **kwargs):
        access_token = get_access_token()
        is_valid, msg, user = verify_token(access_token)

        if not user:
            return {"message": msg}, Unauthorized.code

        return f(*args, **kwargs)

    return decorated


def is_admin(f):
    """
    Check if user is premium.
    """

    @wraps(f)
    def decorated(*args, **kwargs):
        """Use this decorator on API endpoints restricted to admin users."""
        access_token = get_access_token()
        is_valid, msg, user = verify_token(access_token)
        if not user:
            return {"message": msg}, Unauthorized.code

        if user['role'] != 'admin':
            return {"message": Forbidden.description}, Forbidden.code

        return f(*args, **kwargs)

    return decorated


def has_roles(allowed_roles: list):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            access_token = get_access_token()
            is_valid, msg, user = verify_token(access_token)

            if not user:
                return {"message": msg}, Unauthorized.code
            if user['role'] not in allowed_roles:
                return {"message": Forbidden.description}, Forbidden.code

            return f(*args, **kwargs)

        return decorated_function

    return decorator


def has_permission(name: str):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            access_token = get_access_token()
            is_valid, msg, user = verify_token(access_token)

            if not user:
                return {"message": msg}, Unauthorized.code
            role_id = 'abc-xyz'
            if 'roleID' in user:
                role_id = user['roleID']
            user_obj = User(user_id=str(user['_id']), role_id=role_id)
            is_allowed, attributes = __check_permission(name, user_obj)

            if is_allowed is False:
                return {"message": Forbidden.description}, Forbidden.code

            return f(*args, **kwargs)

        return decorated_function

    return decorator


def verify_token(auth_token: str):
    user_repo = UserRepository(Mongo.get_instance())
    auth_service = AuthService(user_repo)

    return auth_service.verify_auth_token(auth_token)
