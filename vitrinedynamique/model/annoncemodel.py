import os
from datetime import datetime
from pynamodb.models import Model
from pynamodb.indexes import AllProjection, GlobalSecondaryIndex
from pynamodb.attributes import (
    UnicodeAttribute, JSONAttribute, ListAttribute
)

ANNONCE_TABLE = os.environ.get('ANNONCE_TABLE', 'VIT-annonce')
TODAY = '%Y-%m-%d'


class AgencesIndex(GlobalSecondaryIndex):
    class Meta:
        index_name = 'agences-index'
        projection = AllProjection()
        read_capacity_units = 5
        write_capacity_units = 5

    agence_id = UnicodeAttribute(hash_key=True)


class AnnonceModel(Model):
    class Meta:
        table_name = ANNONCE_TABLE
        region = 'eu-west-1'

    annonce_id = UnicodeAttribute(hash_key=True)
    agence_id = UnicodeAttribute()
    retrieval_date = UnicodeAttribute(default=datetime.strftime(datetime.today(), TODAY))
    photos = ListAttribute()
    description = UnicodeAttribute()

    index_agences = AgencesIndex()

    def __str__(self):
        return '[AnnonceModel id={} agence={}]'.format(self.annonce_id, self.agence_id)
