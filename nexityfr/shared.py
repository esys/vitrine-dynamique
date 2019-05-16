from typing import Dict, Tuple
from abc import ABC, abstractmethod
import logging
from requests import get

logger = logging.getLogger(__name__)


class Response(ABC):
    def __init__(self, parameters: dict, data: dict):
        self.parameters = parameters
        self.data = data

    def __str__(self):
        return '[Response data={}...]'.format(str(self.data)[:50])


class ListResponse(Response):
    def __init__(self, parameters: dict, data: dict):
        super().__init__(parameters, data)
        self.count = self.data['count']

    def __str__(self):
        return '[ListResponse {} count={}]'.format(super(__class__, self).__str__(), self.count)


class PaginatedResponse(ListResponse):
    pass


class PaginatedResponse(ListResponse):
    def __init__(self, service_callable, parameters: dict, data: dict):
        super().__init__(parameters, data)
        self.service_callable = service_callable
        self.current = self.data['pagination']['current']
        self.page_count = self.data['pagination']['pageCount']
        self.page_size = self.data['pagination']['pageSize']

    def next(self) -> PaginatedResponse:
        if self.current + 1 > self.page_count:
            return None

        new_parameters = self.parameters.copy()
        new_parameters.update({'page_number': self.current + 1})

        return self.service_callable(**new_parameters)

    def __str__(self):
        return '[PaginatedResponse {} page={} pageCount={} pageSize={}]'.format(
            super(__class__, self).__str__(),
            self.current,
            self.page_count,
            self.page_size)


class NexityAPI(ABC):
    NEXITYFR_BASE_URL = 'https://www.nexity.fr/ws-rest/offre'

    FUNCTION_ARG_TO_URL = {
        'page_number': 'pageNumber',
        'page_size': 'pageSize',
        'native_id': 'nativeId',
    }

    def __init__(self, ws: str):
        self.ws = ws

    def _call(self, *args) -> Response:
        url, parameters = self._build_url(args)

        logger.debug(url)
        response = get(url)
        data = response.json()

        return self._get_response(parameters, data)

    def _build_url(self, locals_parameters: Tuple) -> (str, Dict):
        # retain non-None parameters
        parameters = {}
        for name, value in locals_parameters[0].items():
            if name != 'self' and value:
                parameters[name] = value

        pairs = []
        for name, value in parameters.items():
            pairs.append('='.join(
                [name if name not in NexityAPI.FUNCTION_ARG_TO_URL else NexityAPI.FUNCTION_ARG_TO_URL[name],
                 str(value)]))

        return NexityAPI.NEXITYFR_BASE_URL + self.ws + '?' + '&'.join(pairs), parameters

    @abstractmethod
    def _get_response(self, parameters: dict, data: dict) -> Response:
        raise NotImplemented()
