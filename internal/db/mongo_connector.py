import os

from pymongo import MongoClient


class Mongo:
    __instance = None
    __mongo_client = None
    database = None

    def __init__(self):
        mongo_uri = os.environ.get("MONGO_URI")
        db_name = os.environ.get("MONGO_DB_NAME")

        print("starting connect to mongodb")

        self.__mongo_client = MongoClient(mongo_uri)
        self.__instance = self.__mongo_client

        try:
            self.__mongo_client.server_info()
            self.__instance = self.__mongo_client
            self.database = self.__instance[db_name]
            print("connect to mongodb successfully ==== ")
        except Exception as e:
            print("error connection: ", e)

    @staticmethod
    def get_instance():
        if Mongo.__instance is None:
            Mongo.__instance = Mongo()
        return Mongo.__instance
