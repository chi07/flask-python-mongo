import json

from bson import json_util
from flask import jsonify, request
from flask_api import status
from flask_restful import Resource
from werkzeug.exceptions import BadRequest

from internal.http.request.login_request import LoginValidator
from internal.http.request.request import get_json_body


class LoginHandler(Resource):
    auth_service = None

    def __init__(self, **kwargs) -> None:
        self.auth_service = kwargs['service']

    def post(self):
        _, request_body = get_json_body(request)
        validator = LoginValidator(request_body)
        is_valid, payload, errors = validator.validate(request_body)

        if is_valid is False:
            return jsonify({"errors": errors, "status": BadRequest.code, "message": "Bad request"})

        password = payload['password']
        email = payload['email']

        is_ok, token = self.auth_service.authenticate(email, str(password))

        if is_ok is False:
            return jsonify(
                {"errors": "email or password is not valid", "status": BadRequest.code, "message": "Bad request"})

        return jsonify({"data": json.loads(json_util.dumps({"token": token})), "status": status.HTTP_200_OK,
                        "message": "login successfully"})
