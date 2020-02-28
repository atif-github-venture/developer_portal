import os

from flask_script import Manager
from signin import blueprint
from signin.main import create_app

app = create_app(os.getenv('ENV') or 'dev')
app.register_blueprint(blueprint)
app.app_context().push()
manager = Manager(app)


@manager.command
def run():
    app.run()
    # run(host=None, port=None, debug=None, load_dotenv=True, **options)


if __name__ == '__main__':
    manager.run()
