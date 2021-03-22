from validator import validate


class AddUserValidator:
    def __init__(self, data):
        self.data = data

    @staticmethod
    def __get_rules():
        rules = {
            "password": "required",
            "passwordConfirmation": "required",
            "roleID": "required",
            "workspaceID": "required",
            "email": "required|mail",
            "username": "required"
        }
        return rules

    def validate(self, payload: dict):
        rules = self.__get_rules()
        return validate(payload, rules, return_info=True)
