import json


class Serializer(json.JSONEncoder):
    def default(self, o):
        return o.__dict__

