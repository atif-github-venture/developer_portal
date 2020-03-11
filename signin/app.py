import os

from flask_script import Manager

from main import create_app
from flask_restplus import Api
from flask import Blueprint

from main.controller.user_controller import api as user_ns
from main.controller.auth_controller import api as auth_ns
from main.controller.user_controller import _getapi as getuser_ns

blueprint = Blueprint('signin', __name__)

api = Api(blueprint,
          title='Signin API with JWT',
          version='1.0',
          description='api for flask restplus web service'
          )

api.add_namespace(user_ns, path='/user')
api.add_namespace(auth_ns)
api.add_namespace(getuser_ns)
app = create_app(os.getenv('ENV') or 'dev')
app.register_blueprint(blueprint)
app.app_context().push()
manager = Manager(app)


@manager.command
def run():
    app.run(host='0.0.0.0', port='8080')


if __name__ == '__main__':
    manager.run()
