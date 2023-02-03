import json
from src import bestellartikel_controller
from src import bestellung_handler
from tests.helper import event, extract_body, extract_status_code, lambda_response, DEFAULT_TENANT_ID


def test_get_bestellartikelliste_ok(lambda_context, bestellartikel_table):
    item1 = {
        'bezeichnung': "Rotwein",
        "gruppe": "Wein"
    }
    item2 = {
        'bezeichnung': "Weiswein",
        "gruppe": "Wein"
    }
    bestellartikel_controller.create_bestellartikel(DEFAULT_TENANT_ID, item1)
    bestellartikel_controller.create_bestellartikel(DEFAULT_TENANT_ID, item2)

    response = bestellung_handler.handle(
        event('/api/bestellartikel', 'GET'), lambda_context)
    body = extract_body(response)

    assert extract_status_code(response) == 200
    assert len(body) == 2


def test_get_bestellartikelliste_empty_ok(lambda_context, bestellartikel_table):
    response = bestellung_handler.handle(
        event('/api/bestellartikel', 'GET'), lambda_context)
    body = extract_body(response)

    assert extract_status_code(response) == 200
    assert len(body) == 0


def test_get_bestellartikelliste_without_tenant_id_not_ok(lambda_context, bestellartikel_table):
    headers = {
        'Content-Type': 'application/json'
    }
    response = bestellung_handler.handle(
        event('/api/bestellartikel', 'GET', None, None, headers), lambda_context)

    assert response == lambda_response(400, json.dumps(
        {'error_text': 'tenant not present.'}))
