from .. import db


class AccessRules(db.Document):
    # id = db.StringField(primary_key=True, autoincrement=True)
    projectname = db.StringField(unique=True, nullable=False)
    groups = db.ListField(max_length=100)
    users = db.ListField(max_length=100)
    registered_on = db.DateTimeField(nullable=False)
