from validator import validate


class RolePermissionValidator:
    def __init__(self, data):
        self.data = data

    @staticmethod
    def __get_rules():
        rules = {
            "roleID": "required",
            "permissionID": "required",
        }
        return rules

    def validate(self, payload: dict):
        rules = self.__get_rules()
        return validate(payload, rules, return_info=True)
