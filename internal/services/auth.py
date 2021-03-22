import datetime
from typing import Tuple

import jwt
from flask import session
from itsdangerous import BadSignature
from werkzeug.security import check_password_hash

from internal.entities.user import User
from internal.repositories.user import UserRepository


class AuthService(object):
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def set_session_data(self, user: User):
        role_id = None
        workspace_id = None
        if 'roleID' in user:
            role_id = user['roleID']
        if 'workspaceID' in user:
            workspace_id = user['workspaceID']

        user_type = 'workspace'
        if 'userType' in user:
            user_type = user['userType']

        user_data = {
            "id": str(user['_id']),
            "email": user['email'],
            "roleID": role_id,
            "workspaceID": workspace_id,
            "userType": user_type,
            "status": str(user['status']),
        }

        session['current_user'] = user_data

        return user_data

    def authenticate(self, email: str, password: str) -> Tuple[bool, str]:
        user = self.user_repo.get_by_email(email)
        if user is None:
            return False, "user is not existed."

        if check_password_hash(user['password'], password) is False:
            return False, "email or password is not correct. Please try again"

        token = self.__generate_auth_token(user)
        user_data = self.set_session_data(user)

        session['current_user'] = user_data
        return True, token

    @staticmethod
    def __generate_auth_token(user: User):
        """Generate an API auth token for user."""
        token = jwt.encode(
            {'user_id': str(user['_id']), 'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)},
            "secret", algorithm="HS256")
        return token

    def verify_auth_token(self, access_token: str) -> Tuple[bool, str, dict]:
        """Check that user API token is correct."""
        split_token = access_token.split()
        if len(split_token) != 2:
            return False, 'invalid token', {}

        if split_token[0] != 'Bearer':
            return False, 'invalid token', {}

        token = split_token[1]
        try:
            data = jwt.decode(token, "secret", algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return False, 'Token has been expired. Please log in again.', {}
        except jwt.InvalidTokenError:
            return False, 'Invalid token. Please log in again.', {}
        except BadSignature:
            return False, 'invalid token', {}

        user = self.user_repo.get(data['user_id'])
        self.set_session_data(user)
        return True, 'success', user

    @staticmethod
    def get_user():
        return session['current_user']

    def get_user_by_email(self, email: str):
        user = self.user_repo.get_by_email(email)
        if user:
            del user['password']
        return user
