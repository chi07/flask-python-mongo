import json

import bson
from bson import json_util
from flask import jsonify, request
from flask_api import status
from flask_restful import Resource
from werkzeug.exceptions import BadRequest, NotFound

from internal.http.middlewares.auth import auth, has_roles, is_admin
from internal.http.request.request import get_json_body
from internal.http.request.user_permission import UserPermissionValidator


class AddUserPermissionHandler(Resource):
    def __init__(self, **kwargs) -> None:
        self.user_permission_service = kwargs['service']

    @auth
    @is_admin
    @has_roles(['admin', 'manager'])
    def post(self):
        _, request_body = get_json_body(request)

        validator = UserPermissionValidator(request_body)
        is_valid, payload, errors = validator.validate(request_body)

        if is_valid is False:
            return jsonify({"errors": errors, "status": BadRequest.code, "message": BadRequest.description})

        email = payload['email']
        permission_id = payload['permission_id']
        attributes = None
        if 'attributes' in request_body:
            attributes = request_body['attributes']

        user = self.user_permission_service.user_repo.get_by_email(email)
        if not user:
            return jsonify(
                {"status": NotFound.code, "message": "user not found"})

        if not bson.ObjectId.is_valid(permission_id):
            return jsonify(
                {"status": NotFound.code, "message": "permissionID is not valid"})

        user_id = str(user['_id'])
        permission_id = str(permission_id)
        permission = self.user_permission_service.permission_repo.get(permission_id)

        if not permission:
            return jsonify(
                {"status": NotFound.code, "message": "cannot found this permission."})

        permission = self.user_permission_service.user_permission_repo.get_user_permission(user_id, permission_id)
        if permission:
            return jsonify(
                {"status": BadRequest.code, "message": "the permission was granted to user."})

        is_ok, p = self.user_permission_service.add_user_permission(user_id, permission_id, attributes)
        if is_ok is False:
            return {"message": is_ok}, BadRequest.code

        return jsonify({"data": json.loads(json_util.dumps({"permission": p})), "status": status.HTTP_200_OK,
                        "message": "add user permission successfully"})
