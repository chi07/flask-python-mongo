from flask import jsonify
from flask_api import status
from flask_restful import Resource
from werkzeug.exceptions import BadRequest

from internal.http.middlewares.auth import auth, has_roles, is_admin


class DeletePermissionHandler(Resource):
    permission_service = None

    def __init__(self, **kwargs) -> None:
        self.permission_service = kwargs['service']

    @auth
    @is_admin
    @has_roles(['admin', 'manager'])
    def delete(self, permission_id):
        permission = self.permission_service.get_by_id(permission_id)
        if not permission:
            return jsonify(
                {"status": BadRequest.code, "message": "permission_id is not valid. cannot found"})

        is_ok = self.permission_service.delete_permission(permission_id)
        if is_ok is False:
            return {"message": is_ok}, BadRequest.code

        return jsonify({"status": status.HTTP_200_OK,
                        "message": "delete permission successfully"})
