import json

import bson
from bson import json_util
from flask import jsonify, request
from flask_api import status
from flask_restful import Resource
from werkzeug.exceptions import BadRequest

from internal.http.middlewares.auth import auth, has_roles, is_admin
from internal.http.request.permission_edit import EditPermissionValidator
from internal.http.request.request import get_json_body


class EditPermissionHandler(Resource):
    permission_service = None

    def __init__(self, **kwargs) -> None:
        self.permission_service = kwargs['service']

    @auth
    @is_admin
    @has_roles(['admin', 'manager'])
    def put(self, permission_id):
        _, request_body = get_json_body(request)

        if not bson.ObjectId.is_valid(permission_id):
            return jsonify({"status": BadRequest.code, "message": "permission_id is not valid"})

        validator = EditPermissionValidator(request_body)
        is_valid, payload, errors = validator.validate(request_body)

        if is_valid is False:
            return jsonify({"errors": errors, "status": BadRequest.code, "message": BadRequest.description})

        permission = self.permission_service.get_by_id(permission_id)
        if not permission:
            return jsonify(
                {"status": BadRequest.code, "message": "permission_id is not valid. cannot found"})

        data = {
            'name': payload['name'],
            'resource': payload['resource'],
            'description': payload['description'],
            'status': permission['status'],
        }

        is_ok = self.permission_service.update_permission(permission_id, data)
        if is_ok is False:
            return {"message": is_ok}, BadRequest.code

        return jsonify({"data": json.loads(json_util.dumps({"permission": permission})), "status": status.HTTP_200_OK,
                        "message": "update permission successfully"})
