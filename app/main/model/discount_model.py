import logging as log

from .. import db
from sqlalchemy.exc import SQLAlchemyError

class Discount_Model(db.Model):
    """ Discount model for storing discount related details """
    __tablename__ = "discounts"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    state_code = db.Column(db.String(10), nullable = False)
    quote_type = db.Column(db.String(10), nullable = False)
    min_km = db.Column(db.Float(precision = 2), nullable = False)
    discount = db.Column(db.Float(precision = 2), nullable = False)
    updated_at = db.Column(db.DateTime, nullable = False)

    def get_discounts_by_state_and_quote_type(self, state_code, quote_type) -> dict:
        """ Gets discounts for state and quote type """
        try:
            discounts = self.query.filter_by(
                state_code = state_code
            ).filter_by(
                quote_type = quote_type
            ).all()
        except SQLAlchemyError as e:
            log.error(e)
            return {
                'status': 'ERROR',
                'message': str(e)
            }
        return {
            'status': 'OK',
            'data': discounts
        }

    def create_discount_bulk(self, data) -> dict:
        """ Creates several discounts by bulk """
        try:
            for discount in data:
                new_discount = Discount_Model(
                    state_code = discount['state_code'],
                    quote_type = discount['quote_type'],
                    min_km = discount['min_km'],
                    discount = discount['discount'],
                    updated_at = discount['updated_at']
                )
                db.session.add(new_discount)
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