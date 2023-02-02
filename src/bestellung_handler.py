from aws_lambda_powertools.event_handler import APIGatewayHttpResolver
import bestellartikel_controller
from bestellartikel_controller import BestellartikelDTO
from lambda_utils.response_utils import response, empty_response
from lambda_utils.event_utils import extract_body, extract_stichtag, extract_tenant
from lambda_utils.exception import ValidationException
import json
app = APIGatewayHttpResolver()


def handle(event: dict, context: dict):
    return app.resolve(event, context)


@app.post('/api/bestellartikel')
def post():
    event = app.current_event
    tenant_id = extract_tenant(event)
    body = extract_body(event)
    bestellartikel = bestellartikel_controller.create_bestellartikel(tenant_id, body)
    return response(201, bestellartikel.to_json())


@app.put('/api/bestellartikel/<id>')
def put(id):
    event = app.current_event
    tenant_id = extract_tenant(event)
    body = extract_body(event)
    bestellartikel = bestellartikel_controller.update_bestellartikel(tenant_id, id, body)
    return response(200, bestellartikel.to_json())


@app.get('/api/bestellartikel/<id>')
def get(id):
    event = app.current_event
    tenant_id = extract_tenant(event)
    bestellartikel = bestellartikel_controller.get_bestellartikel(tenant_id, id)
    if bestellartikel:
        return response(200, bestellartikel.to_json())
    else:
        return empty_response(404)


@app.get('/api/bestellartikel')
def getAll():
    event = app.current_event
    tenant_id = extract_tenant(event)
    bestellartikelliste = bestellartikel_controller.get_bestellartikelliste(tenant_id)
    return response(200, json.dumps(bestellartikelliste, default=BestellartikelDTO.to_json))


@app.delete('/api/bestellartikel/<id>')
def delete(id):
    event = app.current_event
    tenant_id = extract_tenant(event)
    deleted = bestellartikel_controller.delete_bestellartikel(tenant_id, id)
    if deleted:
        return empty_response(204)
    else:
        return empty_response(404)


@app.exception_handler(ValidationException)
def handle_http_exception(exception: ValidationException):
    return response(exception.http_status, exception.to_json())
