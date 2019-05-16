from typing import List


class Photo:
    def __init__(self, photo_id: str, url: str):
        self.photo_id = photo_id
        self.url = url


class Bien:
    def __init__(self, native_id: str, agence_id: str, description: str, photos: List[Photo]):
        self.native_id = native_id
        self.agence_id = agence_id
        self.description = description
        self.photos = photos

    @staticmethod
    def from_dict(data: dict):
        photos = []
        for p in data['photos']:
            url = p['direct']
            photo_id = url.split('/')[-1]
            photos.append(Photo(photo_id, url))

        return Bien(native_id=data['native_id'], agence_id=data['agence_id'], description=data['description'],
                    photos=photos)


class Agence:
    def __init__(self, agence_id: str, libelle: str):
        self.agence_id = agence_id
        self.libelle = libelle
