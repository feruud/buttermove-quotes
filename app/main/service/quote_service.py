import datetime

from app.main.model.quote_model import Quote_Model
from app.main.model.state_model import State_Model
from app.main.model.discount_model import Discount_Model
from app.main.util.quote_type_enum import Quote_Type_Enum

class Quote_Service:

    def create_quote(self, data) -> tuple:
        """ Creates a new quote """
        # Validate state
        state_model = State_Model()
        state_response = state_model.get_state_by_code(data['state_code'].upper())

        if state_response['status'] == 'ERROR':
            response_object = {
                'status': 'ERROR',
                'message': 'Server error'
            }
            return response_object, 500

        state = state_response['data']

        if not state:
            response_object = {
                'status': 'FAILED',
                'message': 'Unsupported state'
            }
            return response_object, 400
        
        state_fee = state.standard_fee
        if data['quote_type'] == Quote_Type_Enum.PREMIUM.value:
            state_fee = state.premium_fee

        # Get discount for state, quote type, and trip distance
        discount_pct = 0.00
        discount_response = self.__get_discount(data['state_code'], data['quote_type'], data['trip_distance_km'])
        
        if discount_response['status'] == 'ERROR':
            return discount_response, 500

        discount = discount_response['data']

        if discount:
            discount_pct = discount.discount

        # Calculate total price (usd)
        quote_timestamp =  datetime.datetime.now(datetime.timezone.utc)
        
        if (state.state_code in ['TX', 'OH']) & (data['trip_distance_km'] >= 20) & (data['trip_distance_km'] <= 30) :
            total_quote = (data['base_fare_usd'] * (1 - discount_pct)) + (data['base_fare_usd'] * state_fee) * (1 + state.tax)
        else:
            total_quote = ((data['base_fare_usd'] + (data['base_fare_usd'] * state_fee)) * (1 + state.tax)) * (1 - discount_pct)
        
        # Create quote
        quote_model = Quote_Model()
        new_quote = {
            "state_code" : state.state_code,
            "quote_type" : data['quote_type'],
            "trip_distance_km" : data['trip_distance_km'],
            "base_fare_usd" : data['base_fare_usd'],
            "quote_usd" : total_quote,
            "created_at" : quote_timestamp
        }
        quote_response = quote_model.create_quote(new_quote)

        if quote_response['status'] == 'ERROR':
            response_object = {
                'status': 'FAILED',
                'message': 'Server error'
            }
            return response_object, 500

        response_object = {
            'status': 'SUCCESS',
            'data': {
                'quote_usd': total_quote,
                'quote_timestamp': str(quote_timestamp.isoformat())
            }
        }
        return response_object, 201

    def __get_discount(self, state_code, quote_type, trip_distance_km) -> dict:
        """ Gets applicable discount for state, quote type, and trip distance """
        discount_model = Discount_Model()
        discount_response = discount_model.get_discounts_by_state_and_quote_type(state_code, quote_type)

        if discount_response['status'] == 'ERROR':
            return {
                'status': 'ERROR',
                'message': 'Server error'
            }

        # Filter discounts and get those that apply for the trip distance
        discount_list = discount_response['data']
        discount_list = list(filter(lambda d: d.min_km < trip_distance_km, discount_list))

        if not discount_list:
            return {
                'status': 'OK',
                'data': []
            }
        
        # In case there's more than one applicable discount keep the one with more km as minimum
        discount_list.sort(key = lambda d: d.min_km, reverse = True)
        
        return {
            'status': 'OK',
            'data': discount_list[0]
        }