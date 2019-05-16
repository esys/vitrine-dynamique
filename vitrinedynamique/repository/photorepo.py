import logging
from typing import List
from vitrinedynamique.model.photomodel import PhotoModel
from vitrinedynamique.domain.photo import Photo
from vitrinedynamique.shared.repository import Repository, Specification, ByAnnonceIdSpecification, AllSpecification
from vitrinedynamique.repository import mappers

logger = logging.getLogger(__name__)


class PhotoRepositoryFromDatabase(Repository[Photo]):
    def __init__(self):
        self.photoModelToPhoto = mappers.PhotoModelToPhoto()
        self.photoToPhotoModel = mappers.PhotoToPhotoModel()

    def get(self, photo_id: str) -> Photo:
        model = PhotoModel.get(photo_id)
        return self.photoModelToPhoto.map(model)

    def list(self, spec: Specification) -> List[Photo]:
        if type(spec) is ByAnnonceIdSpecification:
            photo_models = PhotoModel.index_annonces.query(spec.annonce_id)
        elif type(spec) is AllSpecification:
            photo_models = PhotoModel.scan()
        else:
            raise ValueError('Unsupported specification ' + str(type(spec)))

        photos = []
        for photo_model in photo_models:
            photo = self.photoModelToPhoto.map(photo_model)
            photos.append(photo)

        return photos

    def save(self, photo: Photo):
        photo_model = self.photoToPhotoModel.map(photo)
        photo_model.save()

    def save_all(self, photos: List[Photo]):
        with PhotoModel.batch_write():
            for photo in photos:
                self.save(photo)
