import uuid
import json
from lambda_utils.validation import check_required_field, check_list_not_empty
from lambda_utils.bool_utils import parse_bool 


def create(item: dict):
    bezeichnung = item.get('bezeichnung')
    check_required_field(bezeichnung, 'bezeichnung')
    beschreibung = item.get('beschreibung')
    preisInEuro = item.get('preisInEuro')
    check_required_field(preisInEuro, 'preisInEuro')
    gruppen = item.get('gruppen')
    check_list_not_empty(gruppen, 'gruppen')
    aktiv = item.get('aktiv')
    return BestellungDTO(
        bezeichnung,
        beschreibung,
        float(preisInEuro),
        gruppen,
        parse_bool(aktiv) if aktiv is not None else True,
        item.get('id')
    )


class BestellungDTO:

    def __init__(self, bezeichnung: str, beschreibung: str, preisInEuro: float, gruppen: list[str], aktiv: bool, id: str = None):
        if id:
            self.id = id
        else:
            self.id = str(uuid.uuid4())
        self.bezeichnung = bezeichnung
        self.beschreibung = beschreibung
        self.preisInEuro = preisInEuro
        self.gruppen = gruppen
        self.aktiv = aktiv

    def to_json(self):
        return json.dumps(self.__dict__)
