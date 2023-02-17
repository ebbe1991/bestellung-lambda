import json
from src import bestellartikel_controller
from src import bestellung_handler
from src.bestellartikel_dto import BestellartikelDTO
from tests.helper import event, lambda_response, DEFAULT_TENANT_ID


def test_update_bestellartikel_ok(lambda_context, bestellartikel_table):
    item = {
        'bezeichnung': "Rotwein",
        "gruppe": "Wein"
    }
    createdBestellartikel = bestellartikel_controller.create_bestellartikel(
        DEFAULT_TENANT_ID, item
    )

    pathParameters = {
        "id": createdBestellartikel.id
    }
    itemUpdate = {
        'bezeichnung': "Rotwein",
        "gruppe": "Wein"
    }
    response = bestellung_handler.handle(event(
        '/api/bestellartikel/{id}', 'PUT', json.dumps(itemUpdate), pathParameters), lambda_context)

    assert response == lambda_response(200, BestellartikelDTO(
        "Rotwein", "Wein", createdBestellartikel.id).to_json())


def test_update_bestellartikel_required_field_to_null_not_ok(lambda_context, bestellartikel_table):
    item = {
        'bezeichnung': "Rotwein",
        "gruppe": "Wein"
    }
    createdBestellartikel = bestellartikel_controller.create_bestellartikel(
        DEFAULT_TENANT_ID, item
    )

    pathParameters = {
        "id": createdBestellartikel.id
    }
    itemUpdate = {
        'bezeichnung': "Rotwein",
        "gruppe": None
    }
    response = bestellung_handler.handle(event(
        '/api/bestellartikel/{id}', 'PUT', json.dumps(itemUpdate), pathParameters), lambda_context)

    assert response == lambda_response(
        400, json.dumps({'error_text': "'gruppe' not present."}))


def test_update_bestellartikel_with_unknown_id_not_ok(lambda_context, bestellartikel_table):
    pathParameters = {
        "id": 'unknown'
    }
    itemUpdate = {
        'bezeichnung': "Rotwein",
        "gruppe": "Wein"
    }
    response = bestellung_handler.handle(event(
        '/api/bestellartikel/{id}', 'PUT', json.dumps(itemUpdate), pathParameters), lambda_context)

    assert response == lambda_response(
        400, json.dumps({'error_text': "unknown id 'unknown' (tenant='mytenant1')."}))


def test_update_bestellartikel_without_body_not_ok(lambda_context, bestellartikel_table):
    item = {
        'bezeichnung': "Rotwein",
        "gruppe": "Wein"
    }
    createdBestellartikel = bestellartikel_controller.create_bestellartikel(
        DEFAULT_TENANT_ID, item)

    pathParameters = {
        "id": createdBestellartikel.id
    }

    response = bestellung_handler.handle(
        event('/api/bestellartikel/{id}', 'PUT', None, pathParameters), lambda_context)

    assert response == lambda_response(400, json.dumps(
        {'error_text': 'body not present.'}))


def test_update_bestellartikel_without_tenant_id_not_ok(lambda_context, bestellartikel_table):
    headers = {
        'Content-Type': 'application/json'
    }
    item = {
        'bezeichnung': "Rotwein",
        "gruppe": "Wein"
    }
    createdBestellartikel = bestellartikel_controller.create_bestellartikel(
        DEFAULT_TENANT_ID, item)

    pathParameters = {
        "id": createdBestellartikel.id
    }
    itemUpdate = {
        'bezeichnung': "Rotwein",
        "gruppe": "Wein"
    }
    response = bestellung_handler.handle(event(
        '/api/bestellartikel/{id}', 'PUT', json.dumps(itemUpdate), pathParameters, headers), lambda_context)

    assert response == lambda_response(400, json.dumps(
        {'error_text': 'tenant not present.'}))
