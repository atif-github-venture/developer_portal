from flask import request
from flask_restplus import Resource
from devportal_flaskapi.main.service.group_service import create_group, get_all_groups, get_group, modify_group
from ..helpers.dto import GroupDto

api = GroupDto.api
group = GroupDto.group


@api.route('')
class Group(Resource):
    @api.doc('group of users')
    @api.expect(group, validate=True)
    @api.response(200, 'Group created.')
    def post(self):
        post_data = request.json
        return create_group(data=post_data)

    @api.doc('get the list of groups')
    @api.marshal_list_with(group, envelope='groupinfo')
    def get(self):
        return get_all_groups()

    @api.doc('modify a group')
    @api.response(200, 'Group updated.')
    def put(self):
        put_data = request.json
        return modify_group(data=put_data)


@api.route('/<group>')
@api.param('group', 'The group identifier')
@api.response(404, 'Group not found.')
class GetGroup(Resource):
    @api.doc('get details of a group')
    @api.marshal_list_with(group)
    def get(self, group):
        groupdetails = get_group(group)
        if not groupdetails:
            api.abort(404)
        else:
            return groupdetails
