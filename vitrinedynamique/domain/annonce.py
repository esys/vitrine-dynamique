from typing import List
from vitrinedynamique.domain.photo import Photo


class Annonce:
    def __init__(self, annonce_id: str):
        self.annonce_id: str = annonce_id
        self.agence_id: str = None
        self.description: str = None
        self.photos: List[Photo] = None

    def __str__(self):
        return '[Annonce id:{} agence_id:{}]'.format(self.annonce_id, self.agence_id)
