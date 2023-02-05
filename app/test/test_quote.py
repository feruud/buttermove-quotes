import unittest

from flask import json
from flask_testing import TestCase
from buttermove_quotes import app
from datetime import datetime

class Test_Quotes(TestCase):
    def create_app(self):
        app.config.from_object('app.main.config.DevelopmentConfig')
        return app

    def test_quotes_post_success_ipv4(self):
        """ Tests /quote/ (POST) with all parameters as expected """
        post_data = {
            "state_code": "CA",
            "quote_type": "PREMIUM",
            "trip_distance_km": 40,
            "base_fare_usd": 100
        }
        post_headers = {
            'Content-Type': 'application/json',
            'ip-client': '127.0.0.1'
        }
        response = self.client.post('/quote/', data = json.dumps(post_data), headers = post_headers)
        response_data = response.json
        self.assertTrue(response_data['status'] == 'SUCCESS')
        self.assertTrue(response_data['data']['quote_usd'] == 126.35)
        self.assertTrue(datetime.fromisoformat(response_data['data']['quote_timestamp']))

    def test_quotes_post_success_ipv6(self):
        """ Tests /quote/ (POST) with all parameters as expected """
        post_data = {
            "state_code": "CA",
            "quote_type": "PREMIUM",
            "trip_distance_km": 40,
            "base_fare_usd": 100
        }
        post_headers = {
            'Content-Type': 'application/json',
            'ip-client': 'fd8d:a9ce:b751:4736:ffff:ffff:ffff:ffff'
        }
        response = self.client.post('/quote/', data = json.dumps(post_data), headers = post_headers)
        response_data = response.json
        self.assertTrue(response_data['status'] == 'SUCCESS')
        self.assertTrue(response_data['data']['quote_usd'] == 126.35)
        self.assertTrue(datetime.fromisoformat(response_data['data']['quote_timestamp']))

    def test_quotes_post_invalid_ip_client_header(self):
        """ Tests /quote/ (POST) with an invalid ip-client header"""
        post_data = {
            "state_code": "CA",
            "quote_type": "PREMIUM",
            "trip_distance_km": 40,
            "base_fare_usd": 100
        }
        post_headers = {
            'Content-Type': 'application/json',
            'ip-client': 'not_an_ip_address'
        }
        response = self.client.post('/quote/', data = json.dumps(post_data), headers = post_headers)
        response_data = response.json
        self.assertTrue(response_data['status'] == 'FAILED')
        self.assertTrue(response_data['message'] == 'ip-client header not valid')

    def test_quotes_post_missing_ip_client_header(self):
        """ Tests /quote/ (POST) without the ip-client header """
        post_data = {
            "state_code": "CA",
            "quote_type": "PREMIUM",
            "trip_distance_km": 40,
            "base_fare_usd": 100
        }
        post_headers = {
            'Content-Type': 'application/json'
        }
        response = self.client.post('/quote/', data = json.dumps(post_data), headers = post_headers)
        response_data = response.json
        self.assertTrue(response_data['status'] == 'FAILED')
        self.assertTrue(response_data['message'] == 'ip-client header missing')

    def test_quotes_post_invalid_state(self):
        """ Tests /quote/ (POST) with an invalid state code """
        post_data = {
            "state_code": "ZZ",
            "quote_type": "PREMIUM",
            "trip_distance_km": 40,
            "base_fare_usd": 100
        }
        post_headers = {
            'Content-Type': 'application/json',
            'ip-client': '127.0.0.1'
        }
        response = self.client.post('/quote/', data = json.dumps(post_data), headers = post_headers)
        response_data = response.json
        self.assertTrue(response_data['status'] == 'FAILED')
        self.assertTrue(response_data['message'] == 'Unsupported state')

    def test_quotes_post_invalid_trip_distance(self):
        """ Tests /quote/ (POST) with an invalid trip distance """
        post_data = {
            "state_code": "CA",
            "quote_type": "PREMIUM",
            "trip_distance_km": -40,
            "base_fare_usd": 100
        }
        post_headers = {
            'Content-Type': 'application/json',
            'ip-client': '127.0.0.1'
        }
        response = self.client.post('/quote/', data = json.dumps(post_data), headers = post_headers)
        response_data = response.json
        self.assertTrue(response_data['errors'])
        self.assertTrue(response_data['message'] == 'Input payload validation failed')

    def test_quotes_post_invalid_base_fare(self):
        """ Tests /quote/ (POST) with an invalid base fare """
        post_data = {
            "state_code": "CA",
            "quote_type": "PREMIUM",
            "trip_distance_km": 40,
            "base_fare_usd": -100
        }
        post_headers = {
            'Content-Type': 'application/json',
            'ip-client': '127.0.0.1'
        }
        response = self.client.post('/quote/', data = json.dumps(post_data), headers = post_headers)
        response_data = response.json
        self.assertTrue(response_data['errors'])
        self.assertTrue(response_data['message'] == 'Input payload validation failed')

    def test_quotes_post_invalid_quote_type(self):
        """ Tests /quote/ (POST) with an invalid quote type """
        post_data = {
            "state_code": "CA",
            "quote_type": "PLATINUM",
            "trip_distance_km": 40,
            "base_fare_usd": 100
        }
        post_headers = {
            'Content-Type': 'application/json',
            'ip-client': '127.0.0.1'
        }
        response = self.client.post('/quote/', data = json.dumps(post_data), headers = post_headers)
        response_data = response.json
        self.assertTrue(response_data['errors'])
        self.assertTrue(response_data['message'] == 'Input payload validation failed')

if __name__ == '__main__':
    unittest.main()