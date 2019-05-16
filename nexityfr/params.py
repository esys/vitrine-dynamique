class Anciennete:
    TOUT = 0
    ANCIEN = 1
    NEUF = 2
    ETUDIANTE = 3
    TERRAIN = 4


class TypeCommercialisation:
    VENTE = 'Vente'
    LOCATION = 'Location'


class TypeBien:
    APPARTEMENT = 'Appartement'
    BUREAUX = 'Bureaux'
    DUPLEX = 'Duplex'
    IMMEUBLE = 'Immeuble'
    LOCAL = 'Local'
    MAISON_VILLA = 'Maison/Villa'
    VILLA = 'Villa'
    PARKING_DOUBLE = 'Parking[]double'
    PARKING_BOX = 'Parking/Box'
    TERRAIN = 'Terrain'
    LOFT_ATELIER_SURFACE = 'Loft/Atelier/Surface'
    COMMERCE = 'Commerce'
    RESIDENCE_ETUDIANT = 'Résidence[]étudiant'
    RESIDENCE_PERSONNES_AGEES = 'Résidence[]personnes[]agées'


class TypeAgence:
    BUREAU = 'bureau'
    AGENCE = 'agence'
    BOUTIQUE = 'boutique'
    TERRAIN = 'terrain'


class ListParam():
    def __init__(self, *values: str):
        self.values = values

    def __str__(self):
        return ','.join([val for val in self.values])


class TypeBienParam(ListParam):
    pass


class AgencesParam(ListParam):
    pass


class TypeAgenceParam(ListParam):
    pass
