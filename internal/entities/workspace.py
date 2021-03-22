from bson.objectid import ObjectId

WORKSPACE_STATUS_ACTIVE = "active"


class Workspace(object):
    def __init__(self, role_id=None, name=None, description=None, status='active',
                 created_at=None, updated_at=None):
        if role_id is None:
            self._id = ObjectId()
        else:
            self._id = role_id
        self.name = name
        self.description = description
        self.status = status
        self.createdAt = created_at
        self.updatedAt = updated_at

    def get_as_json(self):
        return self.__dict__

    @staticmethod
    def build_from_json(json_data):
        if json_data is not None:
            try:
                return Workspace(json_data.get('_id', None),
                                 json_data['name'],
                                 json_data['description'],
                                 json_data['status'])
            except KeyError as e:
                raise Exception("Key not found in json_data: {}".format(e))
        else:
            raise Exception("No data to create Role from!")

    @property
    def id(self):
        return self._id
