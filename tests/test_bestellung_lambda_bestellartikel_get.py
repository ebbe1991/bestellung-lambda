import json
from src import bestellartikel_controller
from src import bestellung_handler
from tests.helper import event, lambda_response, DEFAULT_TENANT_ID


def test_get_bestellartikel_not_found(lambda_context, bestellartikel_table):
    pathParameters = {
        "id": "unknown_id"
    }
    response = bestellung_handler.handle(event(
        '/api/bestellartikel/{id}', 'GET', None, pathParameters), lambda_context)

    assert response == lambda_response(404)


def test_get_bestellartikel_ok(lambda_context, bestellartikel_table):
    item = {
        'bezeichnung': "Rotwein",
        "gruppe": "Wein"
    }
    createdBestellartikel = bestellartikel_controller.create_bestellartikel(
        DEFAULT_TENANT_ID, item)

    pathParameters = {
        "id": createdBestellartikel.id
    }
    response = bestellung_handler.handle(event(
        '/api/bestellartikel/{id}', 'GET', None, pathParameters), lambda_context)

    assert response == lambda_response(200, createdBestellartikel.to_json())

def test_get_bestellartikel_without_tenant_id_not_ok(lambda_context, bestellartikel_table):
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
    response = bestellung_handler.handle(event(
        '/api/bestellartikel/{id}', 'GET', None, pathParameters, headers), lambda_context)

    assert response == lambda_response(400, json.dumps(
        {'error_text': 'tenant not present.'}))
