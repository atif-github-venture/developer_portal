from functools import wraps
from flask import request
from devportal_flaskapi.main.service.auth_helper import Auth
from ..service.permission_service import get_permission


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        data, status = Auth.get_logged_in_user(request)
        token = data.get('data')

        if not token:
            return data, status

        return f(*args, **kwargs)

    return decorated


def view_rights_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        data, status = Auth.get_logged_in_user(request)
        username = data.get('data')['username']
        perm = get_permission(username)
        if 'view' not in perm:
            response_object = {
                'status': 'fail',
                'message': 'Authorization failure.'
            }
            return response_object, 401

        return f(*args, **kwargs)

    return decorated


def dev_rights_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        data, status = Auth.get_logged_in_user(request)
        username = data.get('data')['username']
        perm = get_permission(username)
        if 'developer' not in perm:
            response_object = {
                'status': 'fail',
                'message': 'Authorization failure.'
            }
            return response_object, 401

        return f(*args, **kwargs)

    return decorated


def admin_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        data, status = Auth.get_logged_in_user(request)
        token = data.get('data')

        if not token:
            return data, status

        admin = token.get('admin')
        if not admin:
            response_object = {
                'status': 'fail',
                'message': 'admin token required'
            }
            return response_object, 401

        return f(*args, **kwargs)

    return decorated
