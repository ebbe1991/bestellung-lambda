import uuid
import json
from datetime import date
from lambda_utils.validation import check_required_field


def create(item: dict):
    bezeichnung = item.get('bezeichnung')
    check_required_field(bezeichnung, 'bezeichnung')
    gruppe = item.get('gruppe')
    check_required_field(gruppe, 'gruppe')
    return BestellartikelDTO(
        bezeichnung,
        gruppe,
        item.get('id')
    )


class BestellartikelDTO:

    def __init__(self, bezeichnung: str, gruppe: str, id: str = None):
        if id:
            self.id = id
        else:
            self.id = str(uuid.uuid4())
        self.bezeichnung = bezeichnung
        self.gruppe = gruppe

    def to_json(self):
        return json.dumps(self.__dict__)
