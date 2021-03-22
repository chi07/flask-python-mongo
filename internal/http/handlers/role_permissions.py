import json

import bson
from bson import json_util
from flask import jsonify, request
from flask_api import status
from flask_restful import Resource
from werkzeug.exceptions import BadRequest, NotFound

from internal.http.middlewares.auth import auth, is_admin
from internal.http.request.request import get_json_body
from internal.http.request.role_permission import RolePermissionValidator


class AddRolePermissionHandler(Resource):
    role_permission_service = None

    def __init__(self, **kwargs) -> None:
        self.role_permission_service = kwargs['service']

    @auth
    @is_admin
    def post(self):
        _, request_body = get_json_body(request)

        validator = RolePermissionValidator(request_body)
        is_valid, payload, errors = validator.validate(request_body)

        if is_valid is False:
            return jsonify({"errors": errors, "status": BadRequest.code, "message": BadRequest.description})

        role_id = payload['roleID']
        permission_id = payload['permissionID']

        if not bson.ObjectId.is_valid(permission_id):
            return jsonify(
                {"status": NotFound.code, "message": "permissionID is not valid"})

        if not bson.ObjectId.is_valid(role_id):
            return jsonify(
                {"status": NotFound.code, "message": "roleID is not valid"})

        is_ok, p = self.role_permission_service.add_role_permission(role_id, permission_id)
        if is_ok is False:
            return {"message": is_ok}, BadRequest.code

        return jsonify({"data": json.loads(json_util.dumps({"permission": p})), "status": status.HTTP_200_OK,
                        "message": "add role permission successfully"})
