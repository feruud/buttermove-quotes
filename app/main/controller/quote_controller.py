from flask import request
from flask_restplus import Resource

from ..service.quote_service import Quote_Service
from ..util.dto.quote_dto import Quote_Dto
from ..util.ip_validator import Ip_Validator

api = Quote_Dto.api

@api.route('/')
class Quote(Resource):
    @api.doc('Create a new quote')
    @api.expect(Quote_Dto.quote, validate = True)
    @api.response(201, Quote_Dto.response_201)
    @api.response(400, Quote_Dto.response_400)
    @api.response(500, Quote_Dto.response_500)
    def post(self) -> tuple:
        """ Creates a new quote """
        # Validate ip-client header
        if 'ip-client' in request.headers:
            if Ip_Validator.validate_ip_address(request.headers['ip-client']):

                # Create a new quote
                data = request.json
                quote_service = Quote_Service()
                return quote_service.create_quote(data = data)

            else :
                response_object = {
                    'status': 'FAILED',
                    'message': 'ip-client header not valid'
                }
                return response_object, 400
        else:
            response_object = {
                'status': 'FAILED',
                'message': 'ip-client header missing'
            }
            return response_object, 400