import json
from src import bestellung_controller
from src import bestellung_handler
from tests.helper import event, lambda_response, DEFAULT_TENANT_ID


def test_get_bestellung_not_found(lambda_context, bestellung_table):
    pathParameters = {
        "id": "unknown_id"
    }
    response = bestellung_handler.handle(event(
        '/api/bestellung/{id}', 'GET', None, pathParameters), lambda_context)

    assert response == lambda_response(404)


def test_get_bestellung_ok(lambda_context, bestellung_table):
    item = {
        'bezeichnung': "Weingeschenke",
        'beschreibung': "Auswahl an Weinen mit Keksen",
        "preisInEuro": 19.99,
        "gruppen": ['Wein', 'Kekse'],
        "aktiv": "true"
    }
    createdBestellung = bestellung_controller.create_bestellung(
        DEFAULT_TENANT_ID, item)

    pathParameters = {
        "id": createdBestellung.id
    }
    response = bestellung_handler.handle(event(
        '/api/bestellung/{id}', 'GET', None, pathParameters), lambda_context)

    assert response == lambda_response(200, createdBestellung.to_json())

def test_get_bestellung_without_tenant_id_not_ok(lambda_context, bestellung_table):
    headers = {
        'Content-Type': 'application/json'
    }
    item = {
        'bezeichnung': "Weingeschenke",
        'beschreibung': "Auswahl an Weinen mit Keksen",
        "preisInEuro": 19.99,
        "gruppen": ['Wein', 'Kekse'],
        "aktiv": "true"
    }
    createdBestellung = bestellung_controller.create_bestellung(
        DEFAULT_TENANT_ID, item)

    pathParameters = {
        "id": createdBestellung.id
    }
    response = bestellung_handler.handle(event(
        '/api/bestellung/{id}', 'GET', None, pathParameters, headers), lambda_context)

    assert response == lambda_response(400, json.dumps(
        {'error_text': 'tenant not present.'}))
