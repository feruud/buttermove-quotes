import json

from flask_restplus import Namespace, fields
from app.main.util.quote_type_enum import Quote_Type_Enum

class Quote_Dto:
    api = Namespace('quote', description = 'Quote operations')
    quote = api.model('quote', {
        'state_code': fields.String(required = True, description = 'Quote state', example = 'CA'),
        'quote_type': fields.String(required = True, enum = [x.value for x in Quote_Type_Enum], description = 'Quote type', example = 'PREMIUM'),
        'trip_distance_km': fields.Fixed(decimals = 2, min = 0, required = True, description = 'Trip distance in km', example = 40),
        'base_fare_usd': fields.Fixed(decimals = 2, min = 0, required = True, description = 'Trip base fare in usd', example = 100)
    })
    response_201 = json.dumps(
        {
            'status': 'SUCCESS',
            'data': {
                'quote_usd': 126.35,
                'quote_timestamp': '2023-02-04T00:51:53.688633+00:00'
            }
        }
    )
    response_400 = json.dumps(
        {
            "status": "FAILED",
            "message": "Unsupported state"
        }
    )
    response_500 = json.dumps(
        {
            "status": "ERROR",
            "message": "Server error"
        }
    )