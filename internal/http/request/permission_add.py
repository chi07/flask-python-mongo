from validator import validate


class AddPermissionValidator:
    def __init__(self, data):
        self.data = data

    @staticmethod
    def __get_rules():
        rules = {
            "name": "required",
            "resource": "required",
            "description": "required",
        }
        return rules

    def validate(self, payload: dict):
        rules = self.__get_rules()
        return validate(payload, rules, return_info=True)
