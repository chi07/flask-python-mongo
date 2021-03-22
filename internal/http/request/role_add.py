from validator import validate


class AddRoleValidator:
    def __init__(self, data):
        self.data = data

    @staticmethod
    def __get_rules():
        rules = {
            "name": "required",
            "code": "required",
            "roleID": "required",
            "workspaceID": "required",
            "description": "required",
        }
        return rules

    def validate(self, payload: dict):
        rules = self.__get_rules()
        return validate(payload, rules, return_info=True)
