import json

from bson import json_util
from flask import jsonify, request
from flask_api import status
from flask_restful import Resource
from werkzeug.exceptions import BadRequest

from internal.entities.workspace import Workspace
from internal.http.middlewares.auth import auth, has_roles, is_admin
from internal.http.request.request import get_json_body
from internal.http.request.workspace_add import AddWorkspaceValidator


class AddWorkspaceHandler(Resource):
    workspace_service = None

    def __init__(self, **kwargs) -> None:
        self.workspace_service = kwargs['service']

    @auth
    @is_admin
    @has_roles(['admin', 'manager'])
    def post(self):
        _, request_body = get_json_body(request)

        validator = AddWorkspaceValidator(request_body)

        is_valid, payload, errors = validator.validate(request_body)
        if is_valid is False:
            return jsonify({"errors": errors, "status": BadRequest.code, "message": BadRequest.description})

        new_workspace = Workspace(
            name=payload['name'],
            description=payload['description'],
        )

        is_ok, workspace, message = self.workspace_service.add_workspace(new_workspace)
        if is_ok is False:
            return {"message": message}, BadRequest.code

        return jsonify({"data": json.loads(json_util.dumps({"workspace": workspace})), "status": status.HTTP_200_OK,
                        "message": "create new workspace successfully"})
