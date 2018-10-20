from flask import Flask

# from instance.config import app_configuration


def create_app():
    app = Flask(__name__)
    # app.config.from_object(app_configuration['development'])
    # app.config.from_pyfile('config.py')
    from app.api.v1 import admin_api
    from app.api.v1.views.views import auth_api
    app.register_blueprint(admin_api, url_prefix="/api/v1")
    app.register_blueprint(auth_api, url_prefix="/api/v1/auth")

    return app
