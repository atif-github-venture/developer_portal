from flask import Flask
from flask_mongoengine import MongoEngine
from flask_bcrypt import Bcrypt
from .config import config_by_name
from elasticapm.contrib.flask import ElasticAPM
from elasticapm.handlers.logging import LoggingHandler
from main.helpers.prometheus import setup_metrics

db = MongoEngine()
flask_bcrypt = Bcrypt()

CONTENT_TYPE_LATEST = str('text/plain; version=0.0.4; charset=utf-8')


def create_app(config_name):
    app = Flask(__name__)
    apm_dict = config_by_name[config_name].ELASTIC_APM
    app.config.from_object(config_by_name[config_name])
    db.init_app(app)
    flask_bcrypt.init_app(app)
    apm = ElasticAPM(app, server_url=apm_dict['SERVER_URL'], service_name=apm_dict['SERVICE_NAME'],
                     logging=apm_dict['LOGGING'])
    setup_metrics(app)
    return app
