from typing import List
import logging
from nexityfr import NexityAPIBien, NexityAPIBiens, AgencesParam
from vitrinedynamique.shared.repository import Repository, DatabaseRepository, Specification, AllSpecification, ByAgenceIdSpecification
from vitrinedynamique.repository.photorepo import PhotoRepositoryFromDatabase
from vitrinedynamique.model.annoncemodel import AnnonceModel
from vitrinedynamique.domain.annonce import Annonce
from vitrinedynamique.repository import mappers

logger = logging.getLogger(__name__)


class AnnonceRepositoryFromDatabase(DatabaseRepository[Annonce]):
    def __init__(self):
        self.modelToAnnonce = mappers.AnnonceModelToAnnonce()
        self.annonceToModel = mappers.AnnonceToAnnonceModel()
        self.photoModelToPhoto = mappers.PhotoModelToPhoto()

    def get(self, annonce_id: str) -> Annonce:
        model = AnnonceModel.get(annonce_id)
        annonce = self.modelToAnnonce.map(model)
        photo_repo_db = PhotoRepositoryFromDatabase()
        self._update_photo_with_db(annonce, photo_repo_db)
        return annonce

    def list(self, spec: Specification) -> List[Annonce]:
        if type(spec) is ByAgenceIdSpecification:
            annonce_models = AnnonceModel.index_agences.query(spec.agence_id, **spec.filters)
        elif type(spec) is AllSpecification:
            annonce_models = AnnonceModel.scan()
        else:
            raise ValueError('Unsupported specification ' + str(type(spec)))

        annonces = []
        photo_repo_db = PhotoRepositoryFromDatabase()
        for annonce_model in annonce_models:
            annonce = self.modelToAnnonce.map(annonce_model)
            self._update_photo_with_db(annonce, photo_repo_db)
            annonces.append(annonce)

        return annonces

    def _update_photo_with_db(self, annonce: Annonce,
                              photo_repo_db: PhotoRepositoryFromDatabase = PhotoRepositoryFromDatabase()):
        for photo in annonce.photos:
            photo_from_db = photo_repo_db.get(photo.photo_id)
            photo.copy_from(photo_from_db)

    def save(self, annonce: Annonce):
        annonce_model = self.annonceToModel.map(annonce)
        annonce_model.save()

    def save_all(self, annonces: List[Annonce]):
        with AnnonceModel.batch_write():
            for annonce in annonces:
                self.save(annonce)


class AnnonceRepositoryFromNfr(Repository[Annonce]):
    def __init__(self):
        self.nfrToAnnonce = mappers.BienToAnnonce()

    def get(self, annonce_id: str) -> Annonce:
        api = NexityAPIBien()
        resp: NexityAPIBien.BienResponse = api.get_bien(annonce_id)
        annonce = self.nfrToAnnonce.map(resp.bien)

        return annonce

    def list(self, spec: Specification) -> List[Annonce]:
        api = NexityAPIBiens()
        if type(spec) is ByAgenceIdSpecification:
            page: NexityAPIBien.BiensPage = api.list_biens(agences=AgencesParam(spec.agence_id), **spec.filters)
        elif type(spec) is AllSpecification:
            page: NexityAPIBien.BiensPage = api.list_biens()
        else:
            raise ValueError('Unsupported specification ' + str(type(spec)))

        annonces = []
        while page is not None:
            logger.debug('received ' + str(page))
            for bien in page.biens:
                annonces.append(self.nfrToAnnonce.map(bien))

            page = page.next()

        return annonces
