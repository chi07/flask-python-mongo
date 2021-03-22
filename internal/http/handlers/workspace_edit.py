import json

import bson
from bson import json_util
from flask import jsonify, request
from flask_api import status
from flask_restful import Resource
from werkzeug.exceptions import BadRequest

from internal.http.middlewares.auth import is_admin
from internal.http.request.request import get_json_body
from internal.http.request.workspace_edit import EditWorkspaceValidator


class EditWorkspaceHandler(Resource):
    workspace_service = None

    def __init__(self, **kwargs) -> None:
        self.workspace_service = kwargs['service']

    @is_admin
    def put(self, workspace_id):
        if not bson.ObjectId.is_valid(workspace_id):
            return jsonify({"status": BadRequest.code, "message": "workspace_id is not valid"})

        _, request_body = get_json_body(request)

        validator = EditWorkspaceValidator(request_body)
        is_valid, payload, errors = validator.validate(request_body)
        if is_valid is False:
            return jsonify({"errors": errors, "status": BadRequest.code, "message": BadRequest.description})

        workspace = self.workspace_service.get_by_id(workspace_id)
        if not workspace:
            return jsonify(
                {"status": BadRequest.code, "message": "workspace_id is not valid. cannot found"})

        data = {
            'name': payload['name'],
            'description': payload['description'],
            'status': payload['status'],
        }

        is_ok = self.workspace_service.update_workspace(workspace_id, data)
        if is_ok is False:
            return {"message": is_ok}, BadRequest.code

        return jsonify({"data": json.loads(json_util.dumps({"workspace": workspace})), "status": status.HTTP_200_OK,
                        "message": "update workspace successfully"})
