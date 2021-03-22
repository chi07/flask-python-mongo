from flask import jsonify
from flask_api import status
from flask_restful import Resource
from werkzeug.exceptions import BadRequest

from internal.http.middlewares.auth import auth, has_roles, is_admin


class DeleteRoleHandler(Resource):
    role_repo = None
    role_service = None

    def __init__(self, **kwargs) -> None:
        self.role_service = kwargs['service']

    @auth
    @is_admin
    @has_roles(['admin', 'manager'])
    def delete(self, role_id):
        permission = self.role_service.get_by_id(role_id)
        if not permission:
            return jsonify(
                {"status": BadRequest.code, "message": "role_id is not valid. cannot found"})

        is_ok = self.role_service.delete_role(role_id)
        if is_ok is False:
            return {"message": is_ok}, BadRequest.code

        return jsonify({"status": status.HTTP_200_OK,
                        "message": "delete role successfully"})
