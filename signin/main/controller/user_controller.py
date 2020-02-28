from flask import request
from flask_restplus import Resource

from signin.main.util.decorator import admin_token_required
from ..util.dto import UserDto
from ..service.user_service import save_new_user, get_all_users, get_a_user

api = UserDto.api
_user = UserDto.user


@api.route('/register')
class UserList(Resource):
    @api.doc('list of registered users')
    @admin_token_required
    @api.marshal_list_with(_user, envelope='data')
    def get(self):
        return get_all_users()

    @api.expect(_user, validate=True)
    @api.response(201, 'User successfully created.')
    @api.doc('Register a new user')
    def post(self):
        data = request.json
        resp = save_new_user(data=data)
        return resp


@api.route('/{public_id}')
@api.param('public_id', 'The User identifier')
@api.response(404, 'User not found.')
class User(Resource):
    @api.doc('get a user')
    @api.marshal_with(_user)
    def get(self, public_id):
        user = get_a_user(public_id)
        if not user:
            api.abort(404)
        else:
            return user
