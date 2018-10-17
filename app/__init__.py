from flask import Flask

from instance.config import app_configuration


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_configuration['development'])
    app.config.from_pyfile('config.py')
    from app.api.v1 import admin_api
    app.register_blueprint(admin_api, url_prefix="/api/v1/users")
    # if __name__ == '__main__':
    #     app.run()

    return app