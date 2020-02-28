
from .. import db, flask_bcrypt
import datetime
from ..config import key
import jwt


class User(db.Document):

    # id = db.StringField(primary_key=True, autoincrement=True)
    email = db.StringFiedld(unique=True, nullable=False)
    public_id = db.StringField(max_length=100, unique=True)
    admin = db.BooleanField(nullable=False, default=False)
    username = db.StringField(max_length=50, unique=True)
    password = db.StringField(max_length=100, nullable=False)
    registered_on = db.DateTimeField(nullable=False)

    # @property
    # def password(self):
    #     raise AttributeError('password: write-only field')
    #
    # @password.setter
    # def password(self, password):
    #     self.password_hash = flask_bcrypt.generate_password_hash(password).decode('utf-8')

    @staticmethod
    def set_password(password):
        return flask_bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return flask_bcrypt.check_password_hash(self.password_hash, password)

    @staticmethod
    def encode_auth_token(user_id):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1, seconds=5),
                'iat': datetime.datetime.utcnow(),
                'user': user_id,
                'admin': True
            }
            return jwt.encode(
                payload,
                key,
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, key)
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

    def __repr__(self):
        return "<User '{}'>".format(self.username)
