import json
from src import bestellung_handler
from src.bestellung_dto import BestellungDTO
from tests.helper import event, lambda_response, extract_id


def test_create_bestellung_ok(lambda_context, bestellung_table):
    item = {
        'bezeichnung': "Weingeschenke",
        'beschreibung': "Auswahl an Weinen mit Keksen",
        "preisInEuro": "19.99",
        "gruppen": ['Wein', 'Kekse'],
        "aktiv": True
    }
    response = bestellung_handler.handle(
        event('/api/bestellung', 'POST', json.dumps(item)), lambda_context)

    id = extract_id(response)

    assert id is not None
    assert response == lambda_response(201, BestellungDTO(
        "Weingeschenke", "Auswahl an Weinen mit Keksen", 19.99, ['Wein', 'Kekse'], True, id).to_json())


def test_create_bestellung_ok_with_float_value(lambda_context, bestellung_table):
    item = {
        'bezeichnung': "Weingeschenke",
        'beschreibung': "Auswahl an Weinen mit Keksen",
        "preisInEuro": 19.99,
        "gruppen": ['Wein', 'Kekse'],
        "aktiv": True
    }
    response = bestellung_handler.handle(
        event('/api/bestellung', 'POST', json.dumps(item)), lambda_context)

    id = extract_id(response)

    assert id is not None
    assert response == lambda_response(201, BestellungDTO(
        "Weingeschenke", "Auswahl an Weinen mit Keksen", 19.99, ['Wein', 'Kekse'], True, id).to_json())


def test_create_bestellung_ok_with_aktiv_as_string_ok(lambda_context, bestellung_table):
    item = {
        'bezeichnung': "Weingeschenke",
        'beschreibung': "Auswahl an Weinen mit Keksen",
        "preisInEuro": 19.99,
        "gruppen": ['Wein', 'Kekse'],
        "aktiv": "true"
    }
    response = bestellung_handler.handle(
        event('/api/bestellung', 'POST', json.dumps(item)), lambda_context)

    id = extract_id(response)

    assert id is not None
    assert response == lambda_response(201, BestellungDTO(
        "Weingeschenke", "Auswahl an Weinen mit Keksen", 19.99, ['Wein', 'Kekse'], True, id).to_json())


def test_create_bestellung_missing_field_bezeichnung_bad_request(lambda_context, bestellung_table):
    item = {
        'bezeichnung': None,
        "gruppen": ["Wein"]
    }
    response = bestellung_handler.handle(
        event('/api/bestellung', 'POST', json.dumps(item)), lambda_context)

    assert response == lambda_response(
        400, json.dumps({'error_text': "'bezeichnung' not present."}))


def test_create_bestellung_missing_field_preisInEuro_bad_request(lambda_context, bestellung_table):
    item = {
        'bezeichnung': "Rotwein",
        "gruppen": ["Wein"]
    }
    response = bestellung_handler.handle(
        event('/api/bestellung', 'POST', json.dumps(item)), lambda_context)

    assert response == lambda_response(400, json.dumps(
        {'error_text': "'preisInEuro' not present."}))


def test_create_bestellung_missing_field_gruppen_bad_request(lambda_context, bestellung_table):
    item = {
        'bezeichnung': "Wein",
        "preisInEuro": "5.55"
    }
    response = bestellung_handler.handle(
        event('/api/bestellung', 'POST', json.dumps(item)), lambda_context)

    assert response == lambda_response(
        400, json.dumps({'error_text': "list 'gruppen' is empty."}))


def test_create_bestellung_gruppen_empty_bad_request(lambda_context, bestellung_table):
    item = {
        'bezeichnung': "Wein",
        "preisInEuro": "5.55",
        "gruppen": []
    }
    response = bestellung_handler.handle(
        event('/api/bestellung', 'POST', json.dumps(item)), lambda_context)

    assert response == lambda_response(
        400, json.dumps({'error_text': "list 'gruppen' is empty."}))




def test_create_bestellung_without_body_not_ok(lambda_context, bestellung_table):
    response = bestellung_handler.handle(
        event('/api/bestellung', 'POST'), lambda_context)

    assert response == lambda_response(400, json.dumps(
        {'error_text': 'body not present.'}))


def test_create_bestellung_without_tenant_id_not_ok(lambda_context, bestellung_table):
    headers = {
        'Content-Type': 'application/json'
    }
    item = {
        'bezeichnung': "Rotwein",
        "gruppe": "Wein"
    }
    response = bestellung_handler.handle(
        event('/api/bestellung', 'POST', json.dumps(item), None, headers), lambda_context)

    assert response == lambda_response(400, json.dumps(
        {'error_text': 'tenant not present.'}))
