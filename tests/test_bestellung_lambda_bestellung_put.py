import json
from src import bestellung_controller
from src import bestellung_handler
from src.bestellung_dto import BestellungDTO
from tests.helper import event, lambda_response, DEFAULT_TENANT_ID


def test_update_bestellung_ok(lambda_context, bestellung_table):
    item = {
        'bezeichnung': "Weingeschenke",
        'beschreibung': "Auswahl an Weinen mit Keksen",
        "preisInEuro": 19.99,
        "gruppen": ['Wein', 'Kekse']
    }
    createdBestellung = bestellung_controller.create_bestellung(
        DEFAULT_TENANT_ID, item
    )

    pathParameters = {
        "id": createdBestellung.id
    }
    itemUpdate = {
        'bezeichnung': "Weingeschenke",
        'beschreibung': "Auswahl an Weinen",
        "preisInEuro": 19.99,
        "gruppen": ['Wein'],
        "aktiv": False
    }
    response = bestellung_handler.handle(event(
        '/api/bestellung/{id}', 'PUT', json.dumps(itemUpdate), pathParameters), lambda_context)

    assert response == lambda_response(200, BestellungDTO(
        "Weingeschenke", "Auswahl an Weinen", 19.99, ["Wein"], False, createdBestellung.id).to_json())


def test_update_bestellung_required_field_to_null_not_ok(lambda_context, bestellung_table):
    item = {
        'bezeichnung': "Weingeschenke",
        'beschreibung': "Auswahl an Weinen",
        "preisInEuro": 19.99,
        "gruppen": ['Wein'],
        "aktiv": False
    }
    createdBestellung = bestellung_controller.create_bestellung(
        DEFAULT_TENANT_ID, item
    )

    pathParameters = {
        "id": createdBestellung.id
    }
    itemUpdate = {
        'bezeichnung': "Weingeschenke",
        'beschreibung': "Auswahl an Weinen",
        "preisInEuro": None,
        "gruppen": ['Wein'],
        "aktiv": False
    }
    response = bestellung_handler.handle(event(
        '/api/bestellung/{id}', 'PUT', json.dumps(itemUpdate), pathParameters), lambda_context)

    assert response == lambda_response(
        400, json.dumps({'error_text': "'preisInEuro' not present."}))


def test_update_bestellung_with_unknown_id_not_ok(lambda_context, bestellung_table):
    pathParameters = {
        "id": 'unknown'
    }
    itemUpdate = {
        'bezeichnung': "Weingeschenke",
        'beschreibung': "Auswahl an Weinen",
        "preisInEuro": 15,
        "gruppen": ['Wein'],
        "aktiv": False
    }
    response = bestellung_handler.handle(event(
        '/api/bestellung/{id}', 'PUT', json.dumps(itemUpdate), pathParameters), lambda_context)

    assert response == lambda_response(
        400, json.dumps({'error_text': "unknown id 'unknown' (tenant='mytenant1')."}))


def test_update_bestellung_without_body_not_ok(lambda_context, bestellung_table):
    item = {
        'bezeichnung': "Weingeschenke",
        'beschreibung': "Auswahl an Weinen",
        "preisInEuro": 15,
        "gruppen": ['Wein'],
        "aktiv": False
    }
    createdBestellung = bestellung_controller.create_bestellung(
        DEFAULT_TENANT_ID, item)

    pathParameters = {
        "id": createdBestellung.id
    }

    response = bestellung_handler.handle(
        event('/api/bestellung/{id}', 'PUT', None, pathParameters), lambda_context)

    assert response == lambda_response(400, json.dumps(
        {'error_text': 'body not present.'}))


def test_update_bestellung_without_tenant_id_not_ok(lambda_context, bestellung_table):
    headers = {
        'Content-Type': 'application/json'
    }
    item = {
        'bezeichnung': "Weingeschenke",
        'beschreibung': "Auswahl an Weinen",
        "preisInEuro": 15,
        "gruppen": ['Wein'],
        "aktiv": False
    }
    createdBestellung = bestellung_controller.create_bestellung(
        DEFAULT_TENANT_ID, item)

    pathParameters = {
        "id": createdBestellung.id
    }
    itemUpdate = {
        'bezeichnung': "Weingeschenke",
        'beschreibung': "Auswahl an Weinen",
        "preisInEuro": 15,
        "gruppen": ['Wein'],
        "aktiv": True
    }
    response = bestellung_handler.handle(event(
        '/api/bestellung/{id}', 'PUT', json.dumps(itemUpdate), pathParameters, headers), lambda_context)

    assert response == lambda_response(400, json.dumps(
        {'error_text': 'tenant not present.'}))
