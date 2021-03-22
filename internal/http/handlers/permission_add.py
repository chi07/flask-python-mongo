import json

from bson import json_util
from flask import jsonify, request
from flask_api import status
from flask_restful import Resource
from werkzeug.exceptions import BadRequest

from internal.entities.permission import Permission
from internal.http.middlewares.auth import is_admin
from internal.http.request.permission_add import AddPermissionValidator
from internal.http.request.request import get_json_body


class AddPermissionHandler(Resource):
    permission_service = None

    def __init__(self, **kwargs) -> None:
        self.permission_service = kwargs['service']

    @is_admin
    def post(self):
        _, request_body = get_json_body(request)

        validator = AddPermissionValidator(request_body)

        is_valid, payload, errors = validator.validate(request_body)
        if is_valid is False:
            return jsonify({"errors": errors, "status": BadRequest.code, "message": BadRequest.description})

        permission = Permission(
            name=payload['name'],
            resource=payload['resource'],
            description=payload['description'],
        )

        is_ok, permission, message = self.permission_service.add_permission(permission)
        if is_ok is False:
            return {"message": message}, BadRequest.code

        return jsonify({"data": json.loads(json_util.dumps({"permission": permission})), "status": status.HTTP_200_OK,
                        "message": "create new role successfully"})
