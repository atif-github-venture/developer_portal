from devportal_flaskapi.main.helpers.consul import ConsulRegistration
from devportal_flaskapi.main import create_app
from devportal_flaskapi.main.controller.user_controller import api as user_ns
from devportal_flaskapi.main.controller.auth_controller import api as auth_ns
from devportal_flaskapi.main.controller.user_controller import _getapi as getuser_ns
from devportal_flaskapi.main.controller.group_controller import api as group_ns
from devportal_flaskapi.main.controller.accessrule_controller import api as access_ns
from devportal_flaskapi.main.controller.swagger_controller import api as swagger_ns
from devportal_flaskapi.main.config import config_by_name
from flask_restplus import Api
import prometheus_client
from flask import Blueprint, Response
import os
from flask_script import Manager

blueprint = Blueprint('Developer portal', __name__)
CONTENT_TYPE_LATEST = str('text/plain; version=0.0.4; charset=utf-8')

api = Api(blueprint,
          title='Developer portal',
          version='1.0',
          description='API to support Swagger UI interactions based on flask restplus web service'
          )
config = os.getenv('ENV') or 'dev'
api.add_namespace(user_ns, path='/user')
api.add_namespace(group_ns, path='/group')
api.add_namespace(access_ns, path='/accessrule')
api.add_namespace(auth_ns)
api.add_namespace(getuser_ns)
api.add_namespace(swagger_ns, '/swagger')
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
    c, msg = ConsulRegistration.register_service(consul_dict['host'], consul_dict['port'], 'developer_portal',
                                                 'localhost', 80)
    if not c:
        return False, msg
    app.run(host='0.0.0.0', port=80)


if __name__ == '__main__':
    manager.run()
