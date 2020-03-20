from devportal_flaskapi.main.model.blacklist import BlacklistToken
from .. import db
import datetime


def save_token(token):
    blacklist_token = BlacklistToken(token=token, blacklisted_on=datetime.datetime.now())
    try:
        # insert the token
        db.Document.save(blacklist_token)
        response_object = {
            'status': 'Success',
            'message': 'Successfully logged out.'
        }
        return response_object, 200
    except Exception as e:
        response_object = {
            'status': 'Fail',
            'message': e
        }
        return response_object, 400
