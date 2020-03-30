from devportal_flaskapi.main.model.swagger import Swagger
from devportal_flaskapi.main import db
import datetime


def save_changes(data):
    return db.Document.save(data)


def create_swagger(data):
    swaggerpath = Swagger.objects(path=data['path']).first()
    if not swaggerpath:
        new_swagger = Swagger(
            projectname=data['projectname'],
            path=data['path'],
            tags=data['tags'],
            dependency=data['dependency'],
            swaggerobject=str(data['swaggerobject']),
            status=data['status'],
            registered_on=datetime.datetime.utcnow()
        )
        if save_changes(new_swagger):
            return "Swagger information saved.", 200
        else:
            return "Something went wrong!", 500
    else:
        response_object = {
            'status': 'fail',
            'message': 'This swagger information already exists!',
        }
        return response_object, 409


def get_swagger(path):
    return Swagger.objects(**path).first()


def get_swagger_projectlist():
    projects = []
    for item in Swagger.objects.all():
        projects.append(item['projectname'])
    return list(set(projects))


def get_swaggerlist_for_project(pn):
    swaggerlist = []
    so = Swagger.objects(projectname=pn)
    for item in so:
        swaggerlist.append(item['path'])
    return list(set(swaggerlist))


def modify_swagger(finder, data):
    swaggerpath = Swagger.objects(path=finder).first()
    if not swaggerpath:
        return "Invalid swagger path", 404
    else:
        if swaggerpath.update(set__projectname=data['projectname'], set__path=data['path'], set__tags=data['tags'],
                              set__status=data['status'], set__swaggerobject=str(data['swaggerobject']),
                              set__dependency=data['dependency']):
            return "Swagger updated!", 200
        else:
            return "Something wrong in update body", 500


def modify_swagger_status(finder, status):
    swaggerpath = Swagger.objects(path=finder).first()
    if not swaggerpath:
        return "Invalid swagger path", 404
    else:
        if swaggerpath.update(set__status=status):
            return "Swagger updated for status!", 200
        else:
            return "Something wrong in update body", 500
