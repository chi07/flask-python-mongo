import bson
from flask import jsonify, request
from flask_api import status
from flask_restful import Resource
from werkzeug.exceptions import BadRequest, NotFound

from internal.http.middlewares.auth import auth, is_admin
from internal.http.request.request import get_json_body
from internal.http.request.user_permission import UserPermissionValidator


class RemoveUserPermissionHandler(Resource):
    def __init__(self, **kwargs) -> None:
        self.user_permission_service = kwargs['service']

    @auth
    @is_admin
    def delete(self):
        _, req_body = get_json_body(request)

        validator = UserPermissionValidator(req_body)
        is_valid, payload, errors = validator.validate(req_body)

        if is_valid is False:
            return jsonify({"errors": errors, "status": BadRequest.code, "message": BadRequest.description})

        email = payload['email']
        permission_id = payload['permission_id']
        if not bson.ObjectId.is_valid(permission_id):
            return jsonify(
                {"status": NotFound.code, "message": "permission_id is not valid"})

        user = self.user_permission_service.user_repo.get_by_email(email)
        if not user:
            return jsonify(
                {"status": NotFound.code, "message": "cannot not found your user with email: " + email})

        user_id = str(user['_id'])
        permission_id = str(permission_id)

        result = self.user_permission_service.remove_user_permission(user_id, permission_id)
        message: str
        if result['n'] == 1:
            message = "remove user permission successfully"
        else:
            message = "user permission was deleted already"
        return jsonify({"status": status.HTTP_200_OK,
                        "message": message})
