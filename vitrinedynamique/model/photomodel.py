import os
from pynamodb.models import Model
from pynamodb.indexes import AllProjection, GlobalSecondaryIndex
from pynamodb.constants import STREAM_NEW_IMAGE
from pynamodb.attributes import (
    UnicodeAttribute, ListAttribute
)

PHOTO_TABLE = os.environ.get('PHOTO_TABLE', 'VIT-photo')


class AnnoncesIndex(GlobalSecondaryIndex):
    class Meta:
        index_name = 'annonces-index'
        projection = AllProjection()
        read_capacity_units = 5
        write_capacity_units = 5

    annonce_id = UnicodeAttribute(hash_key=True)


class PhotoModel(Model):
    class Meta:
        table_name = PHOTO_TABLE
        region = 'eu-west-1'
        stream_view_type = STREAM_NEW_IMAGE

    photo_id = UnicodeAttribute(hash_key=True)
    annonce_id = UnicodeAttribute()
    url = UnicodeAttribute()
    tags = ListAttribute(null=True)

    index_annonces = AnnoncesIndex()


    def __str__(self):
        return '[PhotoModel id={} annonce={}]'.format(self.photo_id, self.annonce_id)
