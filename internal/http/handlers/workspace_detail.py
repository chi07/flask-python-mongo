import json

import bson
from bson import json_util
from flask import jsonify, request
from flask_api import status
from flask_restful import Resource
from werkzeug.exceptions import BadRequest

from internal.http.middlewares.auth import auth, is_admin
from internal.http.request.request import get_json_body


class ShowWorkspaceHandler(Resource):
    workspace_service = None

    def __init__(self, **kwargs) -> None:
        self.workspace_service = kwargs['service']

    @auth
    @is_admin
    def get(self, workspace_id):
        _, request_body = get_json_body(request)

        if not bson.ObjectId.is_valid(workspace_id):
            return jsonify({"status": BadRequest.code, "message": "workspace is not valid"})

        workspace = self.workspace_service.get_by_id(workspace_id)
        if workspace is False:
            return {"message": "workspace not found with id: " + workspace_id}, BadRequest.code

        return jsonify({"data": json.loads(json_util.dumps({"workspace": workspace})), "status": status.HTTP_200_OK,
                        "message": "get workspace successfully"})
