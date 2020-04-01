import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'secret_key')
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True
    MONGODB_SETTINGS = {'db': 'microdb',
                        'host': 'localhost',
                        'port': 27017}
    ELASTIC_APM = {
        'SERVICE_NAME': 'developer-portal',
        'SERVER_URL': 'http://localhost:8200',
        'LOGGING': True
    }
    CONSUL = {
        'host': '127.0.0.1',
        'port': '8500'
    }


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    MONGODB_SETTINGS = {'db': 'microdb',
                        'host': 'localhost',
                        'port': 27017}
    ELASTIC_APM = {
        'SERVICE_NAME': 'developer-portal',
        'SERVER_URL': 'http://localhost:8200',
        'LOGGING': True
    }
    CONSUL = {
        'host': '127.0.0.1',
        'port': '8500'
    }


class ProductionConfig(Config):
    DEBUG = False
    MONGODB_SETTINGS = {'db': 'microdb',
                        'host': 'host.docker.internal',
                        'port': 27017}
    ELASTIC_APM = {
        'SERVICE_NAME': 'developer-portal',
        'SERVER_URL': 'http://host.docker.internal:8200',
        'LOGGING': True
    }
    CONSUL = {
        'host': 'host.docker.internal',
        'port': '8500'
    }


config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)

key = Config.SECRET_KEY
