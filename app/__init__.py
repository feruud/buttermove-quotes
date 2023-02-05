# app/__init__.py

from flask_restplus import Api
from flask import Blueprint

from .main.controller.quote_controller import api as quote_ns

blueprint = Blueprint('api', __name__)

api = Api(
    blueprint,
    title = 'Buttermove quote tool',
    version = '1.0',
    description = 'A microservice that creates quotes'
)

api.add_namespace(quote_ns, path='/quote')