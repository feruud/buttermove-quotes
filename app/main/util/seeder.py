import datetime

from app.main import db
from app.main.model.state_model import State_Model
from app.main.model.discount_model import Discount_Model

def seed():
    now = datetime.datetime.utcnow()
    
    # Seed states
    state_model = State_Model()
    state_model.query.delete()
    state_batch = [
        {
            "state_code" : 'NY',
            "state_name" : 'New York',
            "standard_fee" : 0.25,
            "premium_fee" : 0.35,
            "tax" : 0.21,
            "updated_at" : now
        },
        {
            "state_code" : 'CA',
            "state_name" : 'California',
            "standard_fee" : 0.23,
            "premium_fee" : 0.33,
            "tax" : 0.00,
            "updated_at" : now
        },
        {
            "state_code" : 'AZ',
            "state_name" : 'Arizona',
            "standard_fee" : 0.20,
            "premium_fee" : 0.30,
            "tax" : 0.00,
            "updated_at" : now
        },
        {
            "state_code" : 'TX',
            "state_name" : 'Texas',
            "standard_fee" : 0.18,
            "premium_fee" : 0.28,
            "tax" : 0.00,
            "updated_at" : now
        },
        {
            "state_code" : 'OH',
            "state_name" : 'Ohio',
            "standard_fee" : 0.15,
            "premium_fee" : 0.25,
            "tax" : 0.00,
            "updated_at" : now
        }
    ]
    state_model.create_state_bulk(data = state_batch)

    # Seed discounts
    discount_model = Discount_Model()
    discount_model.query.delete()
    discount_batch = [
        {
            "state_code" : 'NY',
            "quote_type" : 'PREMIUM',
            "min_km" : 25,
            "discount" : 0.05,
            "updated_at" : now
        },
        {
            "state_code" : 'CA',
            "quote_type" : 'STANDARD',
            "min_km" : 26,
            "discount" : 0.05,
            "updated_at" : now
        },
        {
            "state_code" : 'AZ',
            "quote_type" : 'STANDARD',
            "min_km" : 26,
            "discount" : 0.05,
            "updated_at" : now
        },
        {
            "state_code" : 'CA',
            "quote_type" : 'PREMIUM',
            "min_km" : 25,
            "discount" : 0.05,
            "updated_at" : now
        },
        {
            "state_code" : 'AZ',
            "quote_type" : 'PREMIUM',
            "min_km" : 25,
            "discount" : 0.05,
            "updated_at" : now
        },
        {
            "state_code" : 'TX',
            "quote_type" : 'STANDARD',
            "min_km" : 20,
            "discount" : 0.03,
            "updated_at" : now
        },
        {
            "state_code" : 'OH',
            "quote_type" : 'STANDARD',
            "min_km" : 20,
            "discount" : 0.03,
            "updated_at" : now
        },
        {
            "state_code" : 'TX',
            "quote_type" : 'STANDARD',
            "min_km" : 30,
            "discount" : 0.05,
            "updated_at" : now
        },
        {
            "state_code" : 'OH',
            "quote_type" : 'STANDARD',
            "min_km" : 30,
            "discount" : 0.05,
            "updated_at" : now
        },
        {
            "state_code" : 'TX',
            "quote_type" : 'PREMIUM',
            "min_km" : 25,
            "discount" : 0.05,
            "updated_at" : now
        },
        {
            "state_code" : 'OH',
            "quote_type" : 'PREMIUM',
            "min_km" : 25,
            "discount" : 0.05,
            "updated_at" : now
        }
    ]

    discount_model.create_discount_bulk(data = discount_batch)