from bestellartikel_dto import BestellartikelDTO, create
from lambda_utils.exception import UnknownIdException
from datetime import date
import dynamo_db_service


def create_bestellartikel(tenant_id: str, dto: dict) -> BestellartikelDTO:
    bestellartikel = create(dto)
    dynamo_db_service.put_bestellartikel(tenant_id, bestellartikel)
    return bestellartikel


def update_bestellartikel(tenant_id: str, id: str, dto: dict) -> BestellartikelDTO:
    dto.update({'id': id})
    bestellartikel = create(dto)
    to_update = get_bestellartikel(tenant_id, id)
    if to_update:
        dynamo_db_service.put_bestellartikel(tenant_id, bestellartikel)
        return bestellartikel
    else:
        raise UnknownIdException(id, tenant_id)


def get_bestellartikel(tenant_id: str, id: str) -> BestellartikelDTO:
    item = dynamo_db_service.get_bestellartikel(tenant_id, id)
    if item:
        bestellartikel = create(item)
        return bestellartikel
    else:
        return None


def get_bestellartikelliste(tenant_id: str, stichtag: date = None) -> list[BestellartikelDTO]:
    bestellartikelliste = []
    items = dynamo_db_service.get_bestellartikelliste(tenant_id)
    for item in items:
        bestellartikel = create(item)
        if stichtag is None or bestellartikel.gueltigBis is None or bestellartikel.gueltigBis >= stichtag:
            bestellartikelliste.append(bestellartikel)
    return bestellartikelliste


def delete_bestellartikel(tenant_id: str, id: str) -> bool:
    bestellartikel = get_bestellartikel(tenant_id, id)
    if bestellartikel:
        dynamo_db_service.delete_bestellartikel(tenant_id, id)
        return True
    else:
        return False
