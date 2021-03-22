import json

import bson
from bson import json_util
from flask import jsonify, request
from flask_api import status
from flask_restful import Resource
from werkzeug.exceptions import BadRequest

from internal.http.request.request import get_json_body


class ListUserHandler(Resource):

    def __init__(self, **kwargs) -> None:
        self.user_service = kwargs['service']

    def get(self):
        _, request_body = get_json_body(request)
        filters = {}
        if 'workspaceID' in request_body:
            if not bson.ObjectId.is_valid(request_body['workspaceID']):
                return jsonify({"status": BadRequest.code, "message": "workspaceID is not valid"})
            filters.update({'workspaceID': request_body['workspaceID']})

        if 'roleID' in request_body:
            if not bson.ObjectId.is_valid(request_body['roleID']):
                return jsonify({"status": BadRequest.code, "message": "roleID is not valid"})
            filters.update({'roleID': request_body['roleID']})

        users = self.user_service.find(filters)

        return jsonify({"data": json.loads(json_util.dumps(users)), "status": status.HTTP_200_OK,
                        "message": "list user successfully"})
