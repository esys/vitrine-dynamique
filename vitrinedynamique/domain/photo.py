from typing import List
from abc import ABC


class Photo(ABC):
    def __init__(self, photo_id: str, annonce_id: str, url: str):
        self.photo_id: str = photo_id
        self.url: str = url
        self.annonce_id = annonce_id

    @staticmethod
    def create(photo_id: str, annonce_id: str, url: str = None, tags: List[str]=None):
        untagged_photo = UntaggedPhoto(photo_id, annonce_id, url)
        if tags and len(tags) > 0:
            return TaggedPhoto.from_untagged_photo(untagged_photo, tags)

        return untagged_photo

    def copy_from(self, other_photo):
        self.__dict__ = other_photo.__dict__.copy() # shallow copy !

    def __str__(self):
        return '[Photo id:{} annonce_id:{} url:{}]'.format(self.annonce_id, self.photo_id, self.url)


class UntaggedPhoto(Photo):
    pass


class TaggedPhoto(UntaggedPhoto):
    pass


class TaggedPhoto(UntaggedPhoto):
    def __init__(self, photo_id: str, annonce_id: str, url: str, tags: List[str]):
        super().__init__(photo_id, annonce_id, url)
        self.tags: List[str] = tags

    @staticmethod
    def from_untagged_photo(untagged_photo: UntaggedPhoto, tags: List[str]) -> TaggedPhoto:
        return TaggedPhoto(untagged_photo.photo_id, untagged_photo.annonce_id, untagged_photo.url, tags)


    def __str__(self):
        return '[TaggedPhoto {} tags:{}]'.format(super(__class__, self).__str__(), self.tags)
