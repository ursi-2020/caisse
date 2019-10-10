[Sommaire](https://ursi-2020.github.io/Documentation/)

Go to: [Endpoints](#endpoints), [Models](#models).

# JSON API

## Get all tickets

Get the tickets registered in the "caisse" db.

**Service name** : `caisse`

**URL** : `api/tickets`

**Method** : `GET`

**Auth required** : NO

**Query Parameters** : NO

**Content examples:**


```json
[
  {
    "id": 42,
    "date": "2019-10-09T17:01:29.408701Z",
    "prix": 424, 
    "client": "33",
    "pointsFidelite": 0,
    "modePaiement": "CASH",
    "articles": ["X1-0", "X1-1"]
  },
  {
    "id": 38,
    "date": "2019-10-09T18:03:45.408701Z",
    "prix": 7582, 
    "client": "22",
    "pointsFidelite": 18,
    "modePaiement": "CARD",
    "articles": ["X1-4", "X1-1"]
  }
]
```