from devportal_flaskapi.main.model.permission import Permission
from devportal_flaskapi.main import db
import datetime


def save_changes(data):
    return db.Document.save(data)


def create_permission(data):
    user = Permission.objects(user=data['user']).first()
    if not user:
        new_permission = Permission(
            user=data['user'],
            permission=data['permission'],
            added_on=datetime.datetime.utcnow()
        )
        if save_changes(new_permission):
            return "Permission created.", 200
        else:
            return "Something went wrong!", 500
    else:
        response_object = {
            'status': 'fail',
            'message': 'User already exists!',
        }
        return response_object, 409


def get_all_permission():
    return list(Permission.objects.all())


def get_permission(user):
    return list(Permission.objects(user=user).first().permission)


def modify_permission(data):
    user = Permission.objects(user=data['user']).first()
    if not user:
        return "Invalid user name", 404
    else:
        if user.update(set__permission=data['permission']):
            return "Permission updated.", 200
        else:
            return "Something wrong in update body", 500
