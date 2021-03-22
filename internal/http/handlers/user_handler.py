import json

from bson import json_util
from flask import jsonify, request
from flask_api import status
from flask_restful import Resource
from werkzeug.exceptions import BadRequest

from internal.entities.user import User
from internal.http.request.request import get_json_body, get_param
from internal.http.request.user_add import AddUserValidator


class AddUserHandler(Resource):

    def __init__(self, **kwargs) -> None:
        self.user_service = kwargs['service']

    def post(self):
        _, request_body = get_json_body(request)

        validator = AddUserValidator(request_body)
        is_valid, _, errors = validator.validate(request_body)
        if is_valid is False:
            return jsonify({"errors": errors, "status": BadRequest.code, "message": "Bad request"})

        user = User(
            name=get_param('name', request_body),
            username=get_param('username', request_body),
            password=get_param('password', request_body),
            email=get_param('email', request_body),
            role_id=get_param('roleID', request_body),
            status=get_param('status', request_body),
            workspace_id=get_param('workspaceID', request_body),
        )

        is_ok, result, msg = self.user_service.add_user(user)
        if is_ok is False:
            return jsonify({"errors": str(msg), "status": BadRequest.code, "message": "Bad request"})

        return jsonify({"data": json.loads(json_util.dumps(result)), "status": status.HTTP_200_OK,
                        "message": "created user successfully"})
