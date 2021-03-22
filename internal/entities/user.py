from bson.objectid import ObjectId

USER_STATUS_ACTIVE = "active"


class User(object):
    def __init__(self, user_id=None, name=None, username=None, email=None, role_id=None, workspace_id=None,
                 status='active', password=None,
                 created_at=None, updated_at=None):
        if user_id is None:
            self._id = ObjectId()
        else:
            self._id = user_id
        self.username = username
        self.name = name
        self.email = email
        self.roleID = role_id
        self.workspaceID = workspace_id
        self.status = status
        self.password = password
        self.created_at = created_at
        self.updated_at = updated_at

    def get_as_json(self):
        return self.__dict__

    @staticmethod
    def build_from_json(json_data):
        if json_data is not None:
            try:
                return User(json_data.get('_id', None),
                            json_data['name'],
                            json_data['email'],
                            json_data['role'],
                            json_data['role_id'],
                            json_data['password'],
                            json_data['status'])
            except KeyError as e:
                raise Exception("Key not found in json_data: {}".format(e))
        else:
            raise Exception("No data to create User from!")

    @property
    def id(self):
        return self._id
