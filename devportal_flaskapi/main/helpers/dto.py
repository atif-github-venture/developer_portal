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

class GroupDto:
    api = Namespace('group', description='Group related operations')
    group = api.model('group', {
        'groupname': fields.String(required=True, description='group name'),
        'users': fields.List(fields.String, required=True, description='users belonging to group')
    })


class AccessDto:
    api = Namespace('projectaccess', description='Access rules for project')
    access = api.model('projectaccess', {
        'projectname': fields.String(required=True, description='name of the project'),
        'groups': fields.List(fields.String, required=True, description='List of groups having visibility to project'),
        'users': fields.List(fields.String, required=True, description='List of users having visibility to project')
    })