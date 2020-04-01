from flask import request, jsonify
from flask_restplus import Resource
from ..service.swagger_service import create_swagger, get_swagger, modify_swagger, \
    modify_swagger_status, get_swagger_projectlist, get_swaggerlist_for_project, get_swagger_metrics
from ..helpers.decorator import token_required, view_rights_required, dev_rights_required
from ..helpers.dto import SwaggerDto
from urllib.parse import parse_qs

api = SwaggerDto.api
swagger = SwaggerDto.swagger

@api.route('')
class SwaggerPost(Resource):
    @api.doc('To save swagger information')
    # @api.expect(swagger, validate=True)
    @token_required
    @dev_rights_required
    @api.response(200, 'Swagger information saved.')
    def post(self):
        post_data = request.json
        return create_swagger(data=post_data)

    @api.doc('Get details of a SINGLE swagger')
    @api.response(404, 'Swagger details not found.')
    @api.marshal_with(swagger)
    @token_required
    @view_rights_required
    def get(self, ):
        query_params = dict(parse_qs(request.query_string))
        query_params = {k.decode("utf-8"): v[0].decode("utf-8") for k, v in query_params.items()}
        if len(query_params) == 0:
            api.abort(404)
        swaggerdetails = get_swagger(query_params)
        if not swaggerdetails:
            api.abort(404)
        else:
            return swaggerdetails


@api.route('/project')
@api.doc('get list of projects for swaggers')
class GetSwaggerProject(Resource):
    @token_required
    @view_rights_required
    def get(self):
        swaggerproject = get_swagger_projectlist()
        if not swaggerproject:
            api.abort(404)
        else:
            return swaggerproject


@api.route('/metrics')
@api.doc('get metrics for dashboard')
class GetSwaggerMetrics(Resource):
    @token_required
    def get(self):
        status = ['Published', 'Deployed', 'Deprecated']
        swaggermetrics = get_swagger_metrics(status)
        if not swaggermetrics:
            api.abort(404)
        else:
            return swaggermetrics


@api.route('/project/<projectname>')
@api.param('projectname', 'project name')
@api.response(404, 'List not found')
class GetSwaggerList(Resource):
    @api.doc('Get a list of swagger for a project')
    @view_rights_required
    @token_required
    def get(self, projectname):
        ms = get_swaggerlist_for_project(projectname)
        if not ms:
            api.abort(404)
        else:
            return ms


@api.route('/status/<swaggerpath>/<status>')
@api.param('swaggerpath', 'status', 'The swagger identifier and status')
@api.response(200, 'Swagger updated.')
@api.response(404, 'Swagger not found.')
class ModifySwaggerStatus(Resource):
    @token_required
    @dev_rights_required
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
    @token_required
    @dev_rights_required
    def put(self):
        swaggerpath = request.args.get('path')
        ms = modify_swagger(swaggerpath, data=request.json)
        if not ms:
            api.abort(404)
        else:
            return ms
