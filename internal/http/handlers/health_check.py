from flask import Response
from flask_restful import Resource


class HealthCheckHandler(Resource):
    @staticmethod
    def get():
        return Response("OK", status=200, mimetype='application/json')
