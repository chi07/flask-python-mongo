import json

import bson
from bson import json_util
from flask import jsonify, request
from flask_api import status
from flask_restful import Resource
from werkzeug.exceptions import BadRequest

from internal.http.middlewares.auth import auth, has_roles, is_admin
from internal.http.request.request import get_json_body
from internal.http.request.role_edit import EditRoleValidator


class EditRoleHandler(Resource):
    role_repo = None
    role_service = None

    def __init__(self, **kwargs) -> None:
        self.role_service = kwargs['service']

    @auth
    @is_admin
    @has_roles(['admin', 'manager'])
    def put(self, role_id):
        _, request_body = get_json_body(request)

        if not bson.ObjectId.is_valid(role_id):
            return jsonify({"status": BadRequest.code, "message": "role_id is not valid"})

        validator = EditRoleValidator(request_body)
        is_valid, payload, errors = validator.validate(request_body)

        if is_valid is False:
            return jsonify({"errors": errors, "status": BadRequest.code, "message": BadRequest.description})

        permission = self.role_service.get_by_id(role_id)
        if not permission:
            return jsonify(
                {"status": BadRequest.code, "message": "role_id is not valid. cannot found"})

        data = {
            'name': payload['name'],
            'code': payload['code'],
            'description': payload['description'],
            'status': permission['status'],
        }

        is_ok = self.role_service.update_role(role_id, data)
        if is_ok is False:
            return {"message": is_ok}, BadRequest.code

        return jsonify({"data": json.loads(json_util.dumps({"permission": permission})), "status": status.HTTP_200_OK,
                        "message": "update permission successfully"})
