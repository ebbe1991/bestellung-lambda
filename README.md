# Bestellung-Lambda

## Routen

### Bestellung 

- POST api/bestellung
- GET api/bestellung/<id>
- GET api/bestellung
- PUT api/bestellung/<id>
- DELETE api/bestellung/<id>


### Bestellartikel
- POST api/bestellartikel
- GET api/bestellartikel/<id>
- GET api/bestellartikel
- PUT api/bestellartikel/<id>
- DELETE api/bestellartikel/<id>

## Umgebungsvariablen
| Name                      | Beschreibung                           |
|---------------------------|----------------------------------------|
| BESTELLUNG_TABLE_NAME     | Name der Bestellung DynamoDB-Table     |
| BESTELLARTIKEL_TABLE_NAME | Name der Bestellartikel DynamoDB-Table |
