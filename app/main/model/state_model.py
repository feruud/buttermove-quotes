import logging as log

from .. import db
from sqlalchemy.exc import SQLAlchemyError

class State_Model(db.Model):
    """ State model for storing state related details """
    __tablename__ = "states"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    state_code = db.Column(db.String(10), nullable = False)
    state_name = db.Column(db.String(50), nullable = False)
    standard_fee = db.Column(db.Float(precision = 2), nullable = False)
    premium_fee = db.Column(db.Float(precision = 2), nullable = False)
    tax = db.Column(db.Float(precision = 2), nullable = False)
    updated_at = db.Column(db.DateTime, nullable = False)

    def get_state_by_code(self, state_code) -> dict:
        """ Gets a state by state code """
        try:
            state = self.query.filter_by(state_code = state_code).first()
        except SQLAlchemyError as e:
            log.error(e)
            return {
                'status': 'ERROR',
                'message': str(e)
            }
        return {
            'status': 'OK',
            'data': state
        }

    def create_state_bulk(self, data) -> dict:
        """ Creates several states by bulk """
        try:
            for state in data:
                new_state = State_Model(
                    state_code = state['state_code'],
                    state_name = state['state_name'],
                    standard_fee = state['standard_fee'],
                    premium_fee = state['premium_fee'],
                    tax = state['tax'],
                    updated_at = state['updated_at']
                )
                db.session.add(new_state)
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