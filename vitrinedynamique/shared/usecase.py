from abc import ABC, abstractmethod
import logging
from vitrinedynamique.shared.requestobj import Request
from vitrinedynamique.shared.responseobj import Response, ResponseFailure

logger = logging.getLogger(__name__)


class UseCase(ABC):
    def execute(self, request: Request) -> Response:
        if not request:
            return ResponseFailure.create_from_invalid_request(request)

        try:
            return self.process_request(request)
        except Exception as e:
            logger.exception(str(self.__class__.__name__))
            return ResponseFailure.create_from_exception(e)

    @abstractmethod
    def process_request(self, request: Request) -> Response:
        raise NotImplementedError('Should implement process_request in use case')
