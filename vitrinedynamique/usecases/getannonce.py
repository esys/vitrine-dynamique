import logging
from abc import ABCMeta
from vitrinedynamique.shared.requestobj import ValidRequest, InvalidRequest
from vitrinedynamique.shared.responseobj import Response, ResponseSuccess
from vitrinedynamique.shared.usecase import UseCase
from vitrinedynamique.domain.annonce import Annonce
from vitrinedynamique.repository.annoncerepo import Repository, AnnonceRepositoryFromDatabase, AnnonceRepositoryFromNfr

logger = logging.getLogger(__name__)


class GetAnnonceRequest(ValidRequest):
    def __init__(self, annonce_id: str):
        self.annonce_id = annonce_id

    @staticmethod
    def create(annonce_id):
        invalid_request = InvalidRequest()
        if not annonce_id:
            invalid_request.add_error('Missing annonce_id parameter')

        if invalid_request.has_errors():
            return invalid_request

        return GetAnnonceRequest(annonce_id)


class GetAnnonceUseCase(UseCase):
    def __init__(self, repo: Repository[Annonce]):
        super().__init__()
        self.repo = repo

    def process_request(self, request: GetAnnonceRequest) -> Response:
        annonce = self.repo.get(request.annonce_id)
        return ResponseSuccess(ResponseSuccess.STATUS_OK, annonce)


class GetAnnonceUseCaseFromDatabase(GetAnnonceUseCase):
    def __init__(self):
        super().__init__(AnnonceRepositoryFromDatabase())


class GetAnnonceUseCaseFromNfr(GetAnnonceUseCase):
    def __init__(self):
        super().__init__(AnnonceRepositoryFromNfr())
