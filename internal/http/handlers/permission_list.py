import json

from bson import json_util
from flask import jsonify
from flask_api import status
from flask_restful import Resource

from internal.http.middlewares.auth import auth, has_roles, is_admin


class ListPermissionHandler(Resource):
    permission_service = None

    def __init__(self, **kwargs) -> None:
        self.permission_service = kwargs['service']

    @auth
    @is_admin
    @has_roles(['admin', 'manager'])
    def get(self):
        permissions = self.permission_service.get_all()

        return jsonify({"data": json.loads(json_util.dumps({"permissions": permissions})), "status": status.HTTP_200_OK,
                        "message": "update permission successfully"})
