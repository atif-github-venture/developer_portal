from .. import db


class Swagger(db.Document):
    # id = db.StringField(primary_key=True, autoincrement=True)
    projectname = db.StringField(nullable=False)
    path = db.StringField(unique=True, nullable=False)
    tags = db.ListField(nullable=False)
    status = db.StringField(nullable=False)
    dependency = db.ListField(nullable=False)
    swaggerobject = db.StringField(nullable=False)
    registered_on = db.DateTimeField(nullable=False)
