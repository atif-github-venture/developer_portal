from flask import request
from flask_restplus import Resource
from devportal_flaskapi.main.service.swagger_service import create_swagger, get_swagger, modify_swagger
from ..helpers.dto import SwaggerDto

api = SwaggerDto.api
swagger = SwaggerDto.swagger


@api.route('')
class SwaggerPost(Resource):
    @api.doc('group of users')
    @api.expect(swagger, validate=True)
    @api.response(200, 'Group created.')
    def post(self):
        post_data = request.json
        return create_swagger(data=post_data)


@api.route('/<groupname>')
@api.param('groupname', 'The group identifier')
@api.response(200, 'Group updated.')
@api.response(404, 'Group not found.')
class ModifyGroup(Resource):
    @api.doc('modify a group')
    def put(self, groupname):
        mc = modify_swagger(groupname, data=request.json)
        if not mc:
            api.abort(404)
        else:
            return mc


@api.route('/<swaggerpath>')
@api.param('swaggerpath', 'The swaggerpath identifier')
@api.response(404, 'Swaggerpath not found.')
class SwaggerGet(Resource):
    @api.doc('get details of a swaggerpath')
    @api.marshal_list_with(swagger)
    def get(self, swaggerpath):
        groupdetails = get_swagger(swaggerpath)
        if not groupdetails:
            api.abort(404)
        else:
            return groupdetails
