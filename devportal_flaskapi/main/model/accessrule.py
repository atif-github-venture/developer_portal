from .. import db


class AccessRules(db.Document):
    # id = db.StringField(primary_key=True, autoincrement=True)
    projectname = db.StringField(unique=True, nullable=False)
    groups = db.ListField()
    users = db.ListField()
    registered_on = db.DateTimeField(nullable=False)
