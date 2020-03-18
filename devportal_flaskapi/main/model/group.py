from .. import db


class Groups(db.Document):

    # id = db.StringField(primary_key=True, autoincrement=True)
    groupname = db.StringField(unique=True, nullable=False)
    users = db.ListField(max_length=100)
    registered_on = db.DateTimeField(nullable=False)
