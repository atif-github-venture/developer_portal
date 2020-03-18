from devportal_flaskapi.main.model.group import Groups
from devportal_flaskapi.main import db
import datetime


def save_changes(data):
    db.Document.save(data)


def create_group(data):
    groupname = Groups.objects(groupname=data['groupname']).first()
    if not groupname:
        new_group = Groups(
            groupname=data['groupname'],
            users=data['users'],
            registered_on=datetime.datetime.utcnow()
        )
        save_changes(new_group)
        return "Group created.", 200
    else:
        response_object = {
            'status': 'fail',
            'message': 'Group already exists!',
        }
        return response_object, 409


def get_all_groups():
    return list(Groups.objects.all())


def get_group(grp):
    return Groups.objects(groupname=grp).first()


def modify_group(finder, data):
    groupname = Groups.objects(groupname=finder).first()
    if not groupname:
        return "Invalid group name", 404
    else:
        if groupname.update(set__groupname=data['groupname'], set__users=data['users']):
            # db.Document.modify(query=Groups.objects(groupname=groupname), data)
            return "Group updated.", 200
        else:
            return "Something wrong in update body", 500
