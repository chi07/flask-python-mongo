from bson.objectid import ObjectId

PERMISSION_STATUS_ACTIVE = "active"


class Permission(object):
    def __init__(self, permission_id=None, name=None, actions=None, resource=None, description=None, status='active',
                 created_at=None, updated_at=None):
        if permission_id is None:
            self._id = ObjectId()
        else:
            self._id = permission_id
        self.resource = resource
        self.name = name
        self.actions = actions
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
                return Permission(json_data.get('_id', None),
                                  json_data['name'],
                                  json_data['resource'],
                                  json_data['actions'],
                                  json_data['description'],
                                  json_data['status'])
            except KeyError as e:
                raise Exception("Key not found in json_data: {}".format(e))
        else:
            raise Exception("No data to create Role from!")

    @property
    def id(self):
        return self._id
