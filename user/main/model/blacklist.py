from .. import db


class BlacklistToken(db.Document):
    """
    Token Model for storing JWT tokens
    """

    token = db.StringField(max_length=500, unique=True, nullable=False)
    blacklisted_on = db.DateTimeField(nullable=False)

    def __repr__(self):
        return '<id: token: {}'.format(self.token)

    @staticmethod
    def check_blacklist(auth_token):
        # check whether auth token has been blacklisted
        res = BlacklistToken.objects(token=str(auth_token)).first()
        if res:
            return True
        else:
            return False
