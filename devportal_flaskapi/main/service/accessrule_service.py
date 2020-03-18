from devportal_flaskapi.main.model.accessrule import AccessRules
from devportal_flaskapi.main import db
import datetime


def save_changes(data):
    return db.Document.save(data)


def create_accessrule(data):
    accessrule = AccessRules.objects(projectname=data['projectname']).first()
    if not accessrule:
        new_accessrule = AccessRules(
            projectname=data['projectname'],
            groups=data['groups'],
            users=data['users'],
            registered_on=datetime.datetime.utcnow()
        )
        if save_changes(new_accessrule):
            return "Access rule created.", 200
        else:
            return 'Something went wrong!', 500
    else:
        response_object = {
            'status': 'fail',
            'message': 'Access rule already exists!',
        }
        return response_object, 409


def get_all_accessrule():
    return list(AccessRules.objects.all())


def get_accessrule(grp):
    return AccessRules.objects(projectname=grp).first()


def modify_accessrule(finder, data):
    projectname = AccessRules.objects(projectname=finder).first()
    if not projectname:
        return "Invalid Access rule", 404
    else:
        if projectname.update(set__projectname=data['projectname'], set__users=data['users'],
                              set__groups=data['groups']):
            return "Access rule updated.", 200
        else:
            return "Something wrong in update body", 400
