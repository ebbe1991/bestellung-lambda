import json
from src import bestellartikel_controller
from src import bestellung_handler
from tests.helper import event, lambda_response, DEFAULT_TENANT_ID


def test_delete_bestellartikel_ok(lambda_context, bestellartikel_table):
    item = {
        'bezeichnung': "Rotwein",
        "gruppe": "Wein"
    }
    createdBestellartikel = bestellartikel_controller.create_bestellartikel(
        DEFAULT_TENANT_ID, item)

    bestellartikelliste = bestellartikel_controller.get_bestellartikelliste(DEFAULT_TENANT_ID)
    assert len(bestellartikelliste) == 1

    pathParameters = {
        "id": createdBestellartikel.id
    }
    response = bestellung_handler.handle(event(
        '/api/bestellartikel/{id}', 'DELETE', None, pathParameters), lambda_context)
    
    assert response == lambda_response(204)
    bestellartikelliste = bestellartikel_controller.get_bestellartikelliste(DEFAULT_TENANT_ID)
    assert len(bestellartikelliste) == 0


def test_delete_bestellartikel_not_ok(lambda_context, bestellartikel_table):
    pathParameters = {
        "id": "abc123"
    }
    response = bestellung_handler.handle(event(
        '/api/bestellartikel/{id}', 'DELETE', None, pathParameters), lambda_context)
   
    assert response == lambda_response(404)


def test_delete_bestellartikel_without_tenant_id_not_ok(lambda_context, bestellartikel_table):
    pathParameters = {
        "id": "abc123"
    }
    headers = {
        'Content-Type': 'application/json'
    }
    response = bestellung_handler.handle(event(
        '/api/bestellartikel/{id}', 'DELETE', None, pathParameters, headers), lambda_context)
    
    assert response == lambda_response(400, json.dumps(
        {'error_text': 'tenant not present.'}))
