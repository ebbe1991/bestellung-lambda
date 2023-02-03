import json
from src import bestellung_controller
from src import bestellung_handler
from tests.helper import event, extract_body, extract_status_code, lambda_response, DEFAULT_TENANT_ID


def test_get_bestellungen_ok(lambda_context, bestellung_table):
    item1 = {
        'bezeichnung': "Kekse",
        'beschreibung': "Auswahl an Keksen",
        "preisInEuro": 9,
        "gruppen": ['Kekse']
    }
    item2 = {
        'bezeichnung': "Weingeschenke",
        'beschreibung': "Auswahl an Weinen mit Keksen",
        "preisInEuro": 19.99,
        "gruppen": ['Wein', 'Kekse']
    }
    bestellung_controller.create_bestellung(DEFAULT_TENANT_ID, item1)
    bestellung_controller.create_bestellung(DEFAULT_TENANT_ID, item2)

    response = bestellung_handler.handle(
        event('/api/bestellung', 'GET'), lambda_context)
    body = extract_body(response)

    assert extract_status_code(response) == 200
    assert len(body) == 2


def test_get_bestellungen_empty_ok(lambda_context, bestellung_table):
    response = bestellung_handler.handle(
        event('/api/bestellung', 'GET'), lambda_context)
    body = extract_body(response)

    assert extract_status_code(response) == 200
    assert len(body) == 0


def test_get_bestellungen_without_tenant_id_not_ok(lambda_context, bestellung_table):
    headers = {
        'Content-Type': 'application/json'
    }
    response = bestellung_handler.handle(
        event('/api/bestellung', 'GET', None, None, headers), lambda_context)

    assert response == lambda_response(400, json.dumps(
        {'error_text': 'tenant not present.'}))
