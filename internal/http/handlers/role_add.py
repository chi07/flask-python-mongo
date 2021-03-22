import json

from bson import json_util
from flask import jsonify, request
from flask_api import status
from flask_restful import Resource
from werkzeug.exceptions import BadRequest

from internal.entities.role import Role
from internal.http.middlewares.auth import is_admin
from internal.http.request.request import get_json_body
from internal.http.request.role_add import AddRoleValidator


class AddRoleHandler(Resource):
    role_repo = None
    role_service = None

    def __init__(self, **kwargs) -> None:
        self.role_service = kwargs['service']

    @is_admin
    def post(self):
        _, request_body = get_json_body(request)

        validator = AddRoleValidator(request_body)

        is_valid, payload, errors = validator.validate(request_body)
        if is_valid is False:
            return jsonify({"errors": errors, "status": BadRequest.code, "message": BadRequest.description})

        role = Role(
            name=payload['name'],
            code=payload['code'],
            workspace_id=payload['workspaceID'],
            description=payload['description'],
        )

        is_ok, role, message = self.role_service.add_role(role)
        if is_ok is False:
            return {"message": message}, BadRequest.code

        return jsonify({"data": json.loads(json_util.dumps({"role": role})), "status": status.HTTP_200_OK,
                        "message": "create new role successfully"})
