import bson
from flask import jsonify, request
from flask_api import status
from flask_restful import Resource
from werkzeug.exceptions import BadRequest, NotFound

from internal.http.middlewares.auth import is_admin
from internal.http.request.request import get_json_body
from internal.http.request.role_permission import RolePermissionValidator


class DeleteRolePermissionHandler(Resource):
    role_permission_service = None

    def __init__(self, **kwargs) -> None:
        self.role_permission_service = kwargs['service']

    @is_admin
    def delete(self):
        _, request_body = get_json_body(request)

        validator = RolePermissionValidator(request_body)
        is_valid, payload, errors = validator.validate(request_body)

        if is_valid is False:
            return jsonify({"errors": errors, "status": BadRequest.code, "message": BadRequest.description})

        role_id = payload['roleID']
        permission_id = payload['permissionID']

        if not bson.ObjectId.is_valid(permission_id):
            return jsonify(
                {"status": NotFound.code, "message": "permissionID invalid"})

        if not bson.ObjectId.is_valid(role_id):
            return jsonify(
                {"status": NotFound.code, "message": "roleID invalid"})

        result = self.role_permission_service.remove_role_permission(role_id, permission_id)

        message: str
        if result['n'] == 1:
            message = "remove role permission successfully"
        else:
            message = "role permission was deleted already"
        return jsonify({"status": status.HTTP_200_OK,
                        "message": message})
