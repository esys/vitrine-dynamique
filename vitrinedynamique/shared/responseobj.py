from abc import ABC
import json
from vitrinedynamique.shared.serializers import Serializer
from vitrinedynamique.shared.requestobj import InvalidRequest


class Response(ABC):
    def __init__(self, status, payload):
        self.status = status
        self.payload = payload

    def serialize(self):
        to_serialize = {
            'status': self.status,
            'payload': self.payload
        }
        return json.dumps(to_serialize, cls=Serializer)


class ResponseSuccess(Response):
    STATUS_OK = 'OK'


class ResponseFailure(Response):
    STATUS_ERROR_PARAMETERS = 'ParametersError'
    STATUS_ERROR_SERVER = 'ServerError'

    @staticmethod
    def create_from_invalid_request(invalid_request: InvalidRequest):
        return ResponseFailure(ResponseFailure.STATUS_ERROR_PARAMETERS,
                               '\n'.join(invalid_request.errors))

    @staticmethod
    def create_from_exception(e: Exception):
        return ResponseFailure(ResponseFailure.STATUS_ERROR_SERVER,
                               "{}: {}".format(e.__class__.__name__, str(e)))
