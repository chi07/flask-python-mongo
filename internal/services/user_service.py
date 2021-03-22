from datetime import datetime
from typing import Tuple, Type

import bson
from werkzeug.security import generate_password_hash

from internal.entities.user import USER_STATUS_ACTIVE, User
from internal.repositories.role import RoleRepository
from internal.repositories.user import UserRepository
from internal.repositories.workspace import WorkspaceRepository


class UserService(object):
    def __init__(self, user_repo: UserRepository, role_repo: RoleRepository, workspace_repo: WorkspaceRepository):
        self.user_repo = user_repo
        self.role_repo = role_repo
        self.workspace_repo = workspace_repo

    def add_user(self, user: User) -> Tuple[bool, Type[User], str]:
        # check user has the same email or not
        existed_user = self.get_by_email(user.email)
        if existed_user:
            return False, User, "The email was taken. Please choose other email"

        existed_user = self.get_by_username(user.username)
        if existed_user:
            return False, User, "The username was taken. Please choose other username"

        if not bson.ObjectId.is_valid(user.workspaceID):
            return False, User, "workspaceID is not valid"

        workspace = self.workspace_repo.get(user.workspaceID)
        if not workspace:
            return False, User, "Can not found workspace with the id"

        if not bson.ObjectId.is_valid(user.roleID):
            return False, User, "roleID is not valid"
        role = self.role_repo.get(user.roleID)
        if not role:
            return False, User, "roleID is not valid. Can not found role with the id"

        now = datetime.now()
        user.created_at = now
        user.updated_at = now
        user.status = USER_STATUS_ACTIVE
        user.password = generate_password_hash(user.password)

        return True, self.user_repo.create(user), "Created user successfully"

    def update_user(self, user: User):
        return self.user_repo.create(user)

    def delete_user(self, user: User):
        return self.user_repo.create(user)

    def read_user(self, user: User):
        return self.user_repo.create(user)

    def get_by_email(self, email: str) -> User:
        return self.user_repo.get_by_email(email)

    def get_by_username(self, username: str) -> User:
        return self.user_repo.get_by_username(username)

    def get_by_id(self, user_id: str) -> dict:
        return self.user_repo.get(user_id)

    def find(self, conditions: dict) -> dict:
        return self.user_repo.find(conditions)
