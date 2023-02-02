import json
from datetime import date
from src import bestellung_handler
from src.bestellartikel_dto import BestellartikelDTO
from tests.helper import event, lambda_response, extract_id


def test_create_bestellartikel_ok(lambda_context, dynamodb_table):
    item = {
        'bezeichnung': "Rotwein",
        "preisInEuro": "5.21",
        "gruppe": "Wein"
    }
    response = bestellung_handler.handle(
        event('/api/bestellartikel', 'POST', json.dumps(item)), lambda_context)

    id = extract_id(response)

    assert id is not None
    assert response == lambda_response(201, BestellartikelDTO(
        "Rotwein", 5.21, "Wein", id).to_json())


def test_create_bestellartikel_ok_with_float_value(lambda_context, dynamodb_table):
    item = {
        'bezeichnung': "Rotwein",
        "preisInEuro": 5.21,
        "gruppe": "Wein"
    }
    response = bestellung_handler.handle(
        event('/api/bestellartikel', 'POST', json.dumps(item)), lambda_context)

    id = extract_id(response)

    assert id is not None
    assert response == lambda_response(201, BestellartikelDTO(
        "Rotwein", 5.21, "Wein", id).to_json())


def test_create_bestellartikel_missing_field_bezeichnung_bad_request(lambda_context, dynamodb_table):
    item = {
        'bezeichnung': None,
        "preisInEuro": "5.21",
        "gruppe": "Wein"
    }
    response = bestellung_handler.handle(
        event('/api/bestellartikel', 'POST', json.dumps(item)), lambda_context)

    assert response == lambda_response(
        400, json.dumps({'error_text': "'bezeichnung' not present."}))


def test_create_bestellartikel_missing_field_preisInEuro_bad_request(lambda_context, dynamodb_table):
    item = {
        'bezeichnung': "Rotwein",
        "gruppe": "Wein"
    }
    response = bestellung_handler.handle(
        event('/api/bestellartikel', 'POST', json.dumps(item)), lambda_context)

    assert response == lambda_response(400, json.dumps(
        {'error_text': "'preisInEuro' not present."}))


def test_create_bestellartikel_missing_field_gruppe_bad_request(lambda_context, dynamodb_table):
    item = {
        'bezeichnung': "Rotwein",
        'preisInEuro': 5.55
    }
    response = bestellung_handler.handle(
        event('/api/bestellartikel', 'POST', json.dumps(item)), lambda_context)

    assert response == lambda_response(400, json.dumps(
        {'error_text': "'gruppe' not present."}))


def test_create_bestellartikel_without_body_not_ok(lambda_context, dynamodb_table):
    response = bestellung_handler.handle(
        event('/api/bestellartikel', 'POST'), lambda_context)

    assert response == lambda_response(400, json.dumps(
        {'error_text': 'body not present.'}))


def test_create_bestellartikel_without_tenant_id_not_ok(lambda_context, dynamodb_table):
    headers = {
        'Content-Type': 'application/json'
    }
    item = {
        'bezeichnung': "Rotwein",
        "preisInEuro": 5.21,
        "gruppe": "Wein"
    }
    response = bestellung_handler.handle(
        event('/api/bestellartikel', 'POST', json.dumps(item), None, headers), lambda_context)

    assert response == lambda_response(400, json.dumps(
        {'error_text': 'tenant not present.'}))
