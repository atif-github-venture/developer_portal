import os
from flask_script import Manager
from main.helpers.consul import ConsulRegistration
from main import create_app
from flask_restplus import Api
import prometheus_client
from flask import Blueprint, Response
from main.controller.user_controller import api as user_ns
from main.controller.auth_controller import api as auth_ns
from main.controller.user_controller import _getapi as getuser_ns
from main.config import config_by_name

blueprint = Blueprint('signin', __name__)
CONTENT_TYPE_LATEST = str('text/plain; version=0.0.4; charset=utf-8')

api = Api(blueprint,
          title='Signin API with JWT',
          version='1.0',
          description='api for flask restplus web service'
          )
config = os.getenv('ENV') or 'dev'
api.add_namespace(user_ns, path='/user')
api.add_namespace(auth_ns)
api.add_namespace(getuser_ns)
app = create_app(config)
app.register_blueprint(blueprint)
app.app_context().push()
manager = Manager(app)


@app.route('/metrics/')
def metrics():
    return Response(prometheus_client.generate_latest(), mimetype=CONTENT_TYPE_LATEST)


@manager.command
def run():
    consul_dict = config_by_name[config].CONSUL
    c, msg = ConsulRegistration.register_service(consul_dict['host'], consul_dict['port'], 'user', 'localhost', 8080)
    if not c:
        return False, msg
    app.run(host='0.0.0.0', port=8080)


if __name__ == '__main__':
    manager.run()
