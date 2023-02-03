import json
from src import bestellung_controller
from src import bestellung_handler
from tests.helper import event, lambda_response, DEFAULT_TENANT_ID


def test_delete_bestellung_ok(lambda_context, bestellung_table):
    item = {
        'bezeichnung': "Weingeschenke",
        'beschreibung': "Auswahl an Weinen mit Keksen",
        "preisInEuro": 19.99,
        "gruppen": ['Wein', 'Kekse'],
        "aktiv": "true"
    }
    createdBestellung = bestellung_controller.create_bestellung(
        DEFAULT_TENANT_ID, item)

    bestellungen = bestellung_controller.get_bestellungen(DEFAULT_TENANT_ID)
    assert len(bestellungen) == 1

    pathParameters = {
        "id": createdBestellung.id
    }
    response = bestellung_handler.handle(event(
        '/api/bestellung/{id}', 'DELETE', None, pathParameters), lambda_context)
    
    assert response == lambda_response(204)
    bestellungen = bestellung_controller.get_bestellungen(DEFAULT_TENANT_ID)
    assert len(bestellungen) == 0


def test_delete_bestellung_not_ok(lambda_context, bestellung_table):
    pathParameters = {
        "id": "abc123"
    }
    response = bestellung_handler.handle(event(
        '/api/bestellung/{id}', 'DELETE', None, pathParameters), lambda_context)
   
    assert response == lambda_response(404)


def test_delete_bestellung_without_tenant_id_not_ok(lambda_context, bestellung_table):
    pathParameters = {
        "id": "abc123"
    }
    headers = {
        'Content-Type': 'application/json'
    }
    response = bestellung_handler.handle(event(
        '/api/bestellung/{id}', 'DELETE', None, pathParameters, headers), lambda_context)
    
    assert response == lambda_response(400, json.dumps(
        {'error_text': 'tenant not present.'}))
