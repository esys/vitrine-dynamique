from typing import List
import logging
import requests
from vitrinedynamique.shared.requestobj import ValidRequest, InvalidRequest
from vitrinedynamique.shared.responseobj import Response, ResponseSuccess
from vitrinedynamique.shared.usecase import UseCase
from vitrinedynamique.task.tagannonce import TagPhotoTask
from vitrinedynamique.task.storeannonces import StoreAnnonceTask

logger = logging.getLogger(__name__)


class LaunchTaskRequest(ValidRequest):
    TASK_STORE = 'store'
    TASK_TAG = 'tag'
    TASKS = [TASK_STORE, TASK_TAG]

    def __init__(self, task_name: str, filters: dict):
        self.task_name = task_name
        self.filters = filters

    @staticmethod
    def create(task_name: str, filters: dict = None):
        invalid_request = InvalidRequest()
        if not task_name:
            invalid_request.add_error('Missing task parameter')

        if task_name not in LaunchTaskRequest.TASKS:
            invalid_request.add_error('Unknown task ' + task_name)

        if task_name == LaunchTaskRequest.TASK_TAG and 'photo_id' not in filters:
            invalid_request.add_error('Expected photo_id query parameter')

        if invalid_request.has_errors():
            return invalid_request

        return LaunchTaskRequest(task_name, filters)


class LaunchTaskUseCase(UseCase):
    def process_request(self, request: LaunchTaskRequest) -> Response:
        task = None
        if request.task_name == LaunchTaskRequest.TASK_STORE:
            task = StoreAnnonceTask()
        elif request.task_name == LaunchTaskRequest.TASK_TAG:
            photo_id = request.filters.get('photo_id')
            task = TagPhotoTask(photo_id)
        else:
            raise ValueError('Undefined task ' + request.task_name)

        task.execute()

        return ResponseSuccess(ResponseSuccess.STATUS_OK,
                               {'task': request.task_name, 'filters': request.filters, 'data': task.data()})
