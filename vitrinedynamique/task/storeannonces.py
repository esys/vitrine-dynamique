import logging
from vitrinedynamique.shared.task import Task
from vitrinedynamique.repository.annoncerepo import AnnonceRepositoryFromDatabase, AnnonceRepositoryFromNfr
from vitrinedynamique.shared.repository import ByAgenceIdSpecification
from vitrinedynamique.repository.photorepo import PhotoRepositoryFromDatabase
from nexityfr import Anciennete, TypeCommercialisation

logger = logging.getLogger(__name__)


class StoreAnnonceTask(Task):
    def execute(self):
        annonce_repo_nfr = AnnonceRepositoryFromNfr()
        annonce_repo_db = AnnonceRepositoryFromDatabase()
        photo_repo_db = PhotoRepositoryFromDatabase()

        annonces = annonce_repo_nfr.list(ByAgenceIdSpecification('COM43',
                                                                 {'anciennete': Anciennete.ANCIEN,
                                                                  'type_commercialisation': TypeCommercialisation.VENTE}))
        annonce_repo_db.save_all(annonces)
        photos = [photo for annonce in annonces for photo in annonce.photos]
        photo_repo_db.save_all(photos)


def execute():
    StoreAnnonceTask().execute()
