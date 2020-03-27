import json

from devportal_flaskapi.main.model.user import User
from flask import Response, make_response
from devportal_flaskapi.main.service.blacklist_service import save_token


class Auth:

    @staticmethod
    def login_user(data):
        try:
            # fetch the user data
            user = User.objects(username=data.get('username')).first()
            if user and user.check_password(data.get('password')):
                auth_token = User.encode_auth_token(user.username, user.admin)
                if auth_token:
                    return {'admin': user.admin, 'token': auth_token.decode()}, 200
            else:
                response_object = {
                    'status': 'Fail',
                    'message': 'Email or password does not match.'
                }
                return response_object, 401

        except Exception as e:
            print(e)
            response_object = {
                'status': 'Fail',
                'message': 'Try again'
            }
            return response_object, 500

    @staticmethod
    def validate_user(data):
        if data:
            auth_token = data
        else:
            auth_token = ''
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                msg, code = save_token(token=auth_token)
                if code == 200:
                    auth_token = User.encode_auth_token(resp['user'], resp['admin'])
                    if auth_token:
                        # resp = Response()
                        # resp.status_code = 204
                        # resp.headers.add('Set-Cookie', 'auth-token=' + auth_token.decode())
                        return {'admin': resp['admin'], 'token': auth_token.decode()}
                else:
                    response_object = {
                        'status': 'Fail',
                        'message': msg
                    }
                    return response_object, 500
            else:
                response_object = {
                    'status': 'Fail',
                    'message': resp
                }
                return response_object, 401
        else:
            response_object = {
                'status': 'Fail',
                'message': 'Provide a valid auth token.'
            }
            return response_object, 403

    @staticmethod
    def logout_user(data):
        if data:
            auth_token = data
        else:
            auth_token = ''
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                # mark the token as blacklisted
                return save_token(token=auth_token)
            else:
                response_object = {
                    'status': 'Fail',
                    'message': resp
                }
                return response_object, 401
        else:
            response_object = {
                'status': 'Fail',
                'message': 'Provide a valid auth token.'
            }
            return response_object, 403

    @staticmethod
    def get_logged_in_user(new_request):
        # get the auth token
        auth_token = new_request.headers.get('Authorization')
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                user = User.objects(username=resp['user']).first()
                response_object = {
                    'status': 'success',
                    'data': {
                        'username': user.username,
                        'email': user.email,
                        'admin': user.admin,
                        'registered_on': str(user.registered_on)
                    }
                }
                return response_object, 200
            response_object = {
                'status': 'Fail',
                'message': resp
            }
            return response_object, 401
        else:
            response_object = {
                'status': 'Fail',
                'message': 'Provide a valid auth token.'
            }
            return response_object, 401
