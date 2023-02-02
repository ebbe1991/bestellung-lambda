import os
import boto3
from bestellartikel_dto import BestellartikelDTO
from boto3.dynamodb.conditions import Key


def get_bestellartikelliste_table():
    dynamodb = boto3.resource('dynamodb')
    table_name = os.getenv('BESTELLARTIKEL_TABLE_NAME')
    return dynamodb.Table(table_name)


def put_bestellartikel(tenant_id: str, bestellartikel: BestellartikelDTO):
    table = get_bestellartikelliste_table()
    table.put_item(
        Item={
            'tenant-id': tenant_id,
            'id': bestellartikel.id,
            'bezeichnung': bestellartikel.bezeichnung,
            'preisInEuro': str(bestellartikel.preisInEuro),
            'gruppe': bestellartikel.gruppe
        }
    )


def get_bestellartikel(tenant_id: str, id: str):
    table = get_bestellartikelliste_table()
    result = table.get_item(
        Key={
            "tenant-id": tenant_id,
            "id": id
        }
    )
    return result.get('Item')


def get_bestellartikelliste(tenant_id: str) -> list:
    table = get_bestellartikelliste_table()
    response = table.query(
        KeyConditionExpression=Key('tenant-id').eq(tenant_id)
    )
    return response['Items']

def delete_bestellartikel(tenant_id: str, id: str):
    table = get_bestellartikelliste_table()
    table.delete_item(
        Key={
            "tenant-id": tenant_id,
            "id": id
        }
    )
