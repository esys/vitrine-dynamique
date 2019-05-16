import logging

from vitrinedynamique.domain.annonce import Annonce
from vitrinedynamique.repository.annoncerepo import Repository, AnnonceRepositoryFromDatabase, AnnonceRepositoryFromNfr
from vitrinedynamique.shared.repository import ByAgenceIdSpecification
from vitrinedynamique.shared.requestobj import ValidRequest, InvalidRequest
from vitrinedynamique.shared.responseobj import Response, ResponseSuccess
from vitrinedynamique.shared.usecase import UseCase

logger = logging.getLogger(__name__)


class ListAnnoncesRequest(ValidRequest):
    pass


class ListAnnoncesRequest(ValidRequest):
    def __init__(self, filters: dict):
        self.filters = filters

    @staticmethod
    def create(filters: dict) -> ListAnnoncesRequest:
        invalid_request = InvalidRequest()
        if 'agence_id' not in filters:
            invalid_request.add_error('Missing agence_id parameter')

        if invalid_request.has_errors():
            return invalid_request

        return ListAnnoncesRequest(filters)


class ListAnnoncesUseCase(UseCase):
    def __init__(self, repo: Repository[Annonce]):
        self.repo = repo

    def process_request(self, request: ListAnnoncesRequest) -> Response:
        annonces = self.repo.list(ByAgenceIdSpecification(request.filters.get('agence_id')))
        logger.debug('got %d annonces', len(annonces))
        return ResponseSuccess(ResponseSuccess.STATUS_OK, annonces)


class ListAnnonceUseCaseFromDatabase(ListAnnoncesUseCase):
    def __init__(self):
        super().__init__(AnnonceRepositoryFromDatabase())


class ListAnnonceUseCaseFromNfr(ListAnnoncesUseCase):
    def __init__(self):
        super().__init__(AnnonceRepositoryFromNfr())