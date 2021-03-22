import json

from bson import json_util
from flask import jsonify
from flask_api import status
from flask_restful import Resource

from internal.http.middlewares.auth import is_admin


class ListWorkspaceHandler(Resource):
    workspace_service = None

    def __init__(self, **kwargs) -> None:
        self.workspace_service = kwargs['service']

    @is_admin
    def get(self):
        workspaces = self.workspace_service.get_all()

        return jsonify({"data": json.loads(json_util.dumps({"workspaces": workspaces})), "status": status.HTTP_200_OK,
                        "message": "get workspace successfully"})
