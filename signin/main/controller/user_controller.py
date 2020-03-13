from flask import request
from flask_restplus import Resource
from main.helpers.decorator import admin_token_required
from ..helpers.dto import RegisterDto
from ..helpers.dto import GetUser
from ..service.user_service import register_new_user, get_all_users, get_a_user

api = RegisterDto.api
_user = RegisterDto.user
_getapi = GetUser.api
_getuser = GetUser.user


@api.route('/register')
class UserRegister(Resource):
    @api.expect(_user, validate=True)
    @api.response(201, 'User successfully registered.')
    @api.doc('Register a new user')
    def post(self):
        data = request.json
        resp = register_new_user(data=data)
        return resp


@api.route('')
class UserRegister(Resource):
    @api.doc('list of registered users')
    @admin_token_required
    @api.marshal_list_with(_getuser, envelope='data')
    def get(self):
        return get_all_users()