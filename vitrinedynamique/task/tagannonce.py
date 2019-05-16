import logging
from typing import List
from vitrinedynamique.shared.task import Task
from vitrinedynamique.repository.photorepo import PhotoRepositoryFromDatabase
from vitrinedynamique.domain.photo import UntaggedPhoto, TaggedPhoto
from vitrinedynamique.shared.responseobj import Response, ResponseSuccess, ResponseFailure

import boto3
import requests

logger = logging.getLogger(__name__)


class TagPhotoTask(Task):
    def __init__(self, photo_id):
        self.photo_id = photo_id
        self.rekognition = boto3.client('rekognition')
        self.tags = []

    def execute(self) -> Response:
        photo_repo = PhotoRepositoryFromDatabase()
        photo = photo_repo.get(self.photo_id)
        if type(photo) is UntaggedPhoto:
            photo: UntaggedPhoto
            self.tags = self.rekognize(photo.url)
            tagged_photo = TaggedPhoto.from_untagged_photo(photo, self.tags)
            photo_repo.save(tagged_photo)

    def data(self) -> List:
        return self.tags

    def rekognize(self, url: str) -> List[str]:
        try:
            response = self.rekognition.detect_labels(
                Image={
                    'Bytes': requests.get(url).content,
                },
                MaxLabels=10,
                # MinConfidence=70.0
            )
        except Exception as e:
            logger.error('When rekognizing tags for %s\n%s', url, str(e))

        tags = []
        for label in response['Labels']:
            name = label['Name']
            confidence = label['Confidence']
            logger.debug('tag %s with label %s (confidence=%f)', url, name, confidence)
            tags.append(name)

        return tags


def execute(event, context):
    print('#### EVENT ' + event)
    print('#### CONTEXT ' + context)
