import logging
from vitrinedynamique.shared.requestobj import ValidRequest, InvalidRequest
from vitrinedynamique.shared.responseobj import Response, ResponseSuccess, ResponseFailure
from vitrinedynamique.shared.usecase import UseCase

logger = logging.getLogger(__name__)


class GetHealthRequest(ValidRequest):
    pass


class GetHealthUseCase(UseCase):
    def process_request(self, request: GetHealthRequest) -> Response:
        return ResponseSuccess(ResponseSuccess.STATUS_OK, {'health': 'everything is fine'})
