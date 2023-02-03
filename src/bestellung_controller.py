from bestellung_dto import BestellungDTO, create
from lambda_utils.exception import UnknownIdException
import dynamo_db_service


def create_bestellung(tenant_id: str, dto: dict) -> BestellungDTO:
    bestellung = create(dto)
    dynamo_db_service.put_bestellung(tenant_id, bestellung)
    return bestellung


def update_bestellung(tenant_id: str, id: str, dto: dict) -> BestellungDTO:
    dto.update({'id': id})
    bestellung = create(dto)
    to_update = get_bestellung(tenant_id, id)
    if to_update:
        dynamo_db_service.put_bestellung(tenant_id, bestellung)
        return bestellung
    else:
        raise UnknownIdException(id, tenant_id)


def get_bestellung(tenant_id: str, id: str) -> BestellungDTO:
    item = dynamo_db_service.get_bestellung(tenant_id, id)
    if item:
        bestellung = create(item)
        return bestellung
    else:
        return None


def get_bestellungen(tenant_id: str) -> list[BestellungDTO]:
    bestellungen = []
    items = dynamo_db_service.get_bestellungen(tenant_id)
    for item in items:
        bestellung = create(item)
        bestellungen.append(bestellung)
    return bestellungen


def delete_bestellung(tenant_id: str, id: str) -> bool:
    bestellung = get_bestellung(tenant_id, id)
    if bestellung:
        dynamo_db_service.delete_bestellung(tenant_id, id)
        return True
    else:
        return False
