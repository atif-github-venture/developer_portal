from .. import db


class Permission(db.Document):
    user = db.StringField(nullable=False, unique=True)
    permission = db.ListField(db.StringField(), nullable=False)
    added_on = db.DateTimeField(nullable=False)


