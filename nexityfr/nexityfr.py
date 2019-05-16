import logging
from .params import *
from .domain import Bien, Agence
from .shared import NexityAPI, ListResponse, PaginatedResponse, Response

logger = logging.getLogger(__name__)


class NexityAPIBiens(NexityAPI):
    NEXITYFR_WS_BIENS = '/biens.json'

    def __init__(self):
        super().__init__(NexityAPIBiens.NEXITYFR_WS_BIENS)

    class BiensPage(PaginatedResponse):
        def __init__(self, service_callable, parameters: dict, data: dict):
            super().__init__(service_callable, parameters, data)
            self.biens = []
            for x in self.data['results']:
                annonce = Bien.from_dict(x['0'])
                self.biens.append(annonce)

    def list_biens(self, page_number: int = 1, page_size: int = 30,
                   types_bien: TypeBienParam = TypeBienParam(TypeBien.MAISON_VILLA, TypeBien.APPARTEMENT),
                   anciennete: Anciennete = Anciennete.TOUT,
                   type_commercialisation: TypeCommercialisation = None,
                   agences: AgencesParam = None) -> BiensPage:
        return self._call(locals())

    def _get_response(self, parameters: dict, data: dict) -> BiensPage:
        return NexityAPIBiens.BiensPage(self.list_biens, parameters, data)


class NexityAPIAgences(NexityAPI):
    NEXITYFR_WS_AGENCES = '/agences.json'

    def __init__(self):
        super().__init__(NexityAPIBiens.NEXITYFR_WS_AGENCES)

    class AgencesResponse(ListResponse):
        def __init__(self, parameters: dict, data: dict):
            super().__init__(parameters, data)
            self.agences = []
            for a in data['agences']:
                self.agences.append(Agence(a['id'], a['libelle']))

    def list_agences(self, ville: str = None, code_postal: str = None) -> AgencesResponse:
        return self._call(locals())

    def _get_response(self, parameters: dict, data: dict) -> AgencesResponse:
        return NexityAPIAgences.AgencesResponse(parameters, data)


class NexityAPIBien(NexityAPI):
    NEXITYFR_WS_BIEN = '/bien.json'

    def __init__(self):
        super().__init__(NexityAPIBien.NEXITYFR_WS_BIEN)

    class BienResponse(Response):
        def __init__(self, parameters: dict, data: dict):
            super().__init__(parameters, data)
            self.bien = Bien.from_dict(data)

    def get_bien(self, native_id: str) -> BienResponse:
        return self._call(locals())

    def _get_response(self, parameters: dict, data: dict) -> BienResponse:
        return NexityAPIBien.BienResponse(parameters, data)
