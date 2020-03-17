from flask import request
from flask_restplus import Resource
from main.service.auth_helper import Auth
from ..helpers.dto import AuthDto

api = AuthDto.api
user_auth = AuthDto.user_auth


@api.route('/login')
class UserLogin(Resource):
    @api.doc('user signin')
    @api.expect(user_auth, validate=True)
    def post(self):
        post_data = request.json
        return Auth.login_user(data=post_data)


@api.route('/validate')
class LogoutAPI(Resource):
    @api.doc('validate a user and return fresh cookie')
    @api.response(204, None)
    def post(self):
        auth_header = request.headers.get('Authorization')
        return Auth.validate_user(data=auth_header)


@api.route('/logout')
class LogoutAPI(Resource):
    @api.doc('logout a user')
    def post(self):
        auth_header = request.headers.get('Authorization')
        return Auth.logout_user(data=auth_header)
