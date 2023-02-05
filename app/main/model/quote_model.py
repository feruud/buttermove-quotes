import logging as log

from .. import db
from sqlalchemy.exc import SQLAlchemyError

class Quote_Model(db.Model):
    """ Quote model for storing quote related details """
    __tablename__ = "quotes"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    state_code = db.Column(db.String(10), nullable = False)
    quote_type = db.Column(db.String(25), nullable = False)
    trip_distance_km = db.Column(db.Float(precision = 2), nullable = False)
    base_fare_usd = db.Column(db.Float(precision = 2), nullable = False)
    quote_usd = db.Column(db.Float(precision = 2), nullable = False)
    created_at = db.Column(db.DateTime, nullable = False)

    def create_quote(self, data) -> dict:
        """ Creates a new quote """
        try:
            new_quote = Quote_Model(
                state_code = data['state_code'],
                quote_type = data['quote_type'],
                trip_distance_km = data['trip_distance_km'],
                base_fare_usd = data['base_fare_usd'],
                quote_usd = data['quote_usd'],
                created_at = data['created_at']
            )
            db.session.add(new_quote)
            db.session.commit()
        except SQLAlchemyError as e:
            log.error(e)
            return {
                'status': 'ERROR',
                'message': str(e)
            }
        return {
            'status': 'OK'
        }