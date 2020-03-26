from flask import request, jsonify
from flask_restplus import Resource
from devportal_flaskapi.main.service.swagger_service import create_swagger, get_swagger, modify_swagger, \
    modify_swagger_status
from ..helpers.dto import SwaggerDto
from urllib.parse import parse_qs

api = SwaggerDto.api
swagger = SwaggerDto.swagger


@api.route('')
class SwaggerPost(Resource):
    @api.doc('Swagger Info')
    # @api.expect(swagger, validate=True)
    @api.response(200, 'Swagger information saved.')
    def post(self):
        post_data = request.json
        return create_swagger(data=post_data)

    @api.doc('Get details of a swagger')
    @api.response(404, 'Swagger details not found.')
    @api.marshal_with(swagger)
    def get(self, ):
        query_params = dict(parse_qs(request.query_string))
        query_params = {k.decode("utf-8"): v[0].decode("utf-8") for k, v in query_params.items()}
        swaggerdetails = get_swagger(query_params)
        if not swaggerdetails:
            api.abort(404)
        else:
            return swaggerdetails


@api.route('/status/<swaggerpath>/<status>')
@api.param('swaggerpath', 'status', 'The swagger identifier and status')
@api.response(200, 'Swagger updated.')
@api.response(404, 'Swagger not found.')
class ModifySwaggerStatus(Resource):
    @api.doc('Modify a swagger status for a path')
    def put(self, swaggerpath, status):
        swaggerpath = swaggerpath.replace('#', '/')
        ms = modify_swagger_status(swaggerpath, status)
        if not ms:
            api.abort(404)
        else:
            return ms


@api.route('/edit')
@api.param('swaggerpath', 'The swagger identifier')
@api.response(200, 'Swagger updated.')
@api.response(404, 'Swagger not found.')
class ModifySwagger(Resource):
    @api.doc('Modify a swagger for a path')
    def put(self):
        swaggerpath = request.args.get('path')
        ms = modify_swagger(swaggerpath, data=request.json)
        if not ms:
            api.abort(404)
        else:
            return ms
