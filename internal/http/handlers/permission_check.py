import json

from bson import json_util
from flask import jsonify, request, session
from flask_api import status
from flask_restful import Resource
from werkzeug.exceptions import BadRequest

from internal.http.middlewares.auth import auth
from internal.http.request.permission_check import CheckPermissionValidator
from internal.http.request.request import get_json_body


class CheckPermissionHandler(Resource):

    def __init__(self, **kwargs) -> None:
        self.check_permission_service = kwargs['service']

    @auth
    def post(self):
        _, request_body = get_json_body(request)

        validator = CheckPermissionValidator(request_body)
        is_valid, payload, errors = validator.validate(request_body)
        if is_valid is False:
            return jsonify({"errors": errors, "status": BadRequest.code, "message": BadRequest.description})

        permission_name = payload['permissionName']
        has_permission, message, attributes = self.check_permission_service.check_user_permission(permission_name)

        return jsonify({
            "data": json.loads(json_util.dumps({"attributes": attributes, 'userInfo': session['current_user']})),
            "status": status.HTTP_200_OK,
            "message": message
        })
