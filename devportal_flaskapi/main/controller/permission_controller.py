from flask import request
from flask_restplus import Resource
from ..helpers.decorator import admin_token_required
from ..helpers.dto import PermissionDto
from ..service.permission_service import create_permission, get_all_permission, modify_permission

api = PermissionDto.api
permission = PermissionDto.permission


@api.route('')
class Permission(Resource):
    @api.doc('Create permission for a user')
    @api.expect(permission, validate=True)
    @api.response(200, 'Permission created')
    @admin_token_required
    def post(self):
        post_data = request.json
        return create_permission(data=post_data)

    @api.doc('Get the list of user/permissions')
    @api.marshal_list_with(permission)
    @admin_token_required
    def get(self):
        return get_all_permission()

    @api.doc('Modify permission for a user')
    @api.response(200, 'Permission updated')
    @admin_token_required
    def put(self):
        return modify_permission(data=request.json)