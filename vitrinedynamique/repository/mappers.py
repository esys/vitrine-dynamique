import nexityfr as nfr
from vitrinedynamique.shared.repository import Mapper
from vitrinedynamique.model.annoncemodel import AnnonceModel
from vitrinedynamique.model.photomodel import PhotoModel
from vitrinedynamique.domain.annonce import Annonce
from vitrinedynamique.domain.photo import Photo, TaggedPhoto


class BienToAnnonceModel(Mapper[nfr.Bien, AnnonceModel]):
    def map(self, from_obj: nfr.Bien) -> AnnonceModel:
        annonce_model = AnnonceModel(from_obj.native_id)
        annonce_model.description = from_obj.description
        annonce_model.agence_id = from_obj.agence_id
        annonce_model.photos = [p.photo_id for p in from_obj.photos]

        return annonce_model


class AnnonceModelToAnnonce(Mapper[AnnonceModel, Annonce]):
    def map(self, from_obj: AnnonceModel) -> Annonce:
        annonce = Annonce(from_obj.annonce_id)
        annonce.agence_id = from_obj.agence_id
        annonce.description = from_obj.description

        annonce.photos = []
        for photo_id in from_obj.photos:
            photo = Photo.create(photo_id, from_obj.annonce_id)
            annonce.photos.append(photo)

        return annonce


class AnnonceToAnnonceModel(Mapper[Annonce, AnnonceModel]):
    def map(self, from_obj: Annonce) -> AnnonceModel:
        annonce_model = AnnonceModel(from_obj.annonce_id)
        annonce_model.description = from_obj.description
        annonce_model.agence_id = from_obj.agence_id
        annonce_model.photos = [p.photo_id for p in from_obj.photos]

        return annonce_model


class BienToAnnonce(Mapper[nfr.Bien, Annonce]):
    def map(self, from_obj: nfr.Bien) -> Annonce:
        annonce = Annonce(from_obj.native_id)
        annonce.agence_id = from_obj.agence_id
        annonce.description = from_obj.description
        annonce.photos = []
        for p in from_obj.photos:
            annonce.photos.append(Photo.create(p.photo_id, from_obj.native_id, p.url))

        return annonce


class PhotoModelToPhoto(Mapper[PhotoModel, Photo]):
    def map(self, from_obj: PhotoModel) -> Photo:
        """
           Return a Photo domain object from database data.
           :param photo_model: photo model from database
           :return: TaggedPhoto or UntaggedPhoto depending on database data
        """
        photo = Photo.create(from_obj.photo_id, from_obj.annonce_id, from_obj.url, from_obj.tags)

        return photo


class PhotoToPhotoModel(Mapper[Photo, PhotoModel]):
    def map(self, from_obj: Photo) -> PhotoModel:
        photo_model = PhotoModel(from_obj.photo_id, annonce_id=from_obj.annonce_id, url=from_obj.url)
        if type(from_obj) is TaggedPhoto:
            photo_model.tags = from_obj.tags

        return photo_model
