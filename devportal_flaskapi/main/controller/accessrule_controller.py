# from flask import request
# from flask_restplus import Resource
# from devportal_flaskapi.main.service.accessrule_service import create_accessrule, get_all_accessrule, get_accessrule, \
#     modify_accessrule
# from ..helpers.dto import AccessDto
# from devportal_flaskapi.main.helpers.decorator import admin_token_required
#
# api = AccessDto.api
# access = AccessDto.access
#
#
# @api.route('')
# class Access(Resource):
#     @api.doc('Project access rules of groups/users')
#     @api.expect(access, validate=True)
#     @api.response(200, 'Access rule created.')
#     @admin_token_required
#     def post(self):
#         post_data = request.json
#         return create_accessrule(data=post_data)
#
#     @api.doc('Get the list of access rules')
#     @api.marshal_list_with(access, envelope='accessruleinfo')
#     @admin_token_required
#     def get(self):
#         return get_all_accessrule()
#
#
# @api.route('/<projectname>')
# @api.param('projectname', 'The access rule identifier')
# @api.response(200, 'Access rule updated.')
# @api.response(404, 'Access rule not found.')
# class ModifyAccessRule(Resource):
#     @api.doc('modify an access rule')
#     @admin_token_required
#     def put(self, projectname):
#         mc = modify_accessrule(projectname, data=request.json)
#         if not mc:
#             api.abort(404)
#         else:
#             return mc
#
#
# @api.route('/<accessrule>')
# @api.param('accessrule', 'The access rule identifier')
# @api.response(404, 'Access rule not found.')
# class GetSingleAccess(Resource):
#     @api.doc('get details of an access rule')
#     @api.marshal_list_with(access)
#     @admin_token_required
#     def get(self, accessrule):
#         groupdetails = get_accessrule(accessrule)
#         if not groupdetails:
#             api.abort(404)
#         else:
#             return groupdetails
