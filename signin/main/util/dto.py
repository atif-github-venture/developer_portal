from flask_restplus import Namespace, fields


class RegisterDto:
    api = Namespace('user', description='User related operations')
    user = api.model('register', {
        'email': fields.String(required=True, description='user email address'),
        'username': fields.String(required=True, description='user username'),
        'password': fields.String(required=True, description='user password')
    })

class GetUser:
    api = Namespace('getuser', description='get user list')
    user = api.model('getuser', {
        'email': fields.String(required=True, description='user email address'),
        'username': fields.String(required=True, description='user username')
    })


class AuthDto:
    api = Namespace('auth', description='authentication related operations')
    user_auth = api.model('auth_details', {
        'email': fields.String(required=True, description='The email address'),
        'password': fields.String(required=True, description='The user password '),
    })
