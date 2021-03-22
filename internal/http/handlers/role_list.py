import json

from bson import json_util
from flask import jsonify
from flask_api import status
from flask_restful import Resource

from internal.http.middlewares.auth import auth, has_roles, is_admin


class ListRoleHandler(Resource):
    role_repo = None
    role_service = None

    def __init__(self, **kwargs) -> None:
        self.role_service = kwargs['service']

    @auth
    @is_admin
    @has_roles(['admin', 'manager'])
    def get(self):
        roles = self.role_service.get_all()

        return jsonify({"data": json.loads(json_util.dumps({"roles": roles})), "status": status.HTTP_200_OK,
                        "message": "get list roles successfully"})
