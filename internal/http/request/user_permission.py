from validator import validate


class UserPermissionValidator:
    def __init__(self, data):
        self.data = data

    @staticmethod
    def __get_rules():
        rules = {
            "email": "required",
            "permission_id": "required",
        }
        return rules

    def validate(self, payload: dict):
        rules = self.__get_rules()
        return validate(payload, rules, return_info=True)
