import json
import uuid
import datetime
from flask import Response
from devportal_flaskapi.main import db
from devportal_flaskapi.main.model.user import User


def register_new_user(data):
    user = User.objects(username=data['username']).first()
    email = User.objects(email=data['email']).first()
    if not user and not email:
        new_user = User(
            public_id=str(uuid.uuid4()),
            email=data['email'],
            username=data['username'],
            admin=False,
            password=User.set_password(data['password']),
            registered_on=datetime.datetime.utcnow()
        )
        if save_changes(new_user):
            return generate_token(new_user)
        else:
            return 'Something went wrong!', 500
    else:
        response_object = {
            'status': 'fail',
            'message': 'User already exists. Please Log in.',
        }
        return response_object, 409


def get_all_users():
    return list(User.objects.all())


def get_a_user(user_name):
    return User.objects(username=user_name).first()


def generate_token(user):
    try:
        # generate the auth token
        auth_token = User.encode_auth_token(user.username, user.admin)
        response_object = {
            'status': 'success',
            'message': 'Successfully registered.'
        }
        resp = Response()
        resp.response = json.dumps(response_object)
        resp.status_code = 200
        resp.headers.add('Set-Cookie', 'auth-token=' + auth_token.decode())
        return resp
    except Exception as e:
        response_object = {
            'status': 'fail',
            'message': 'Some error occurred. Please try again.'
        }
        return response_object, 401


def save_changes(data):
    return db.Document.save(data)
