from flask import Flask
from flask_mongoengine import MongoEngine
from flask_bcrypt import Bcrypt
from .config import config_by_name
from elasticapm.contrib.flask import ElasticAPM
from elasticapm.handlers.logging import LoggingHandler

db = MongoEngine()
flask_bcrypt = Bcrypt()


def create_app(config_name):
    app = Flask(__name__)
    apm = ElasticAPM(app, server_url='http://apm-server:8200', service_name='auth-service', logging=True)
    app.config.from_object(config_by_name[config_name])
    db.init_app(app)
    flask_bcrypt.init_app(app)
    return app
