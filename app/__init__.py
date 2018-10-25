from flask import Flask, make_response, jsonify


def create_app():
    app = Flask(__name__)
    from app.api.v1 import version_api as v1
    from app.api.v1.views.views import landing_page
    app.register_blueprint(v1, url_prefix="/api/v1")
    app.register_blueprint(landing_page)

    @app.errorhandler(404)
    def not_found(e):
        """Catch 404 errors"""
        return make_response(jsonify({
            "Message": "Route not found. Please check on the route"
        }), 200)

    @app.errorhandler(500)
    def internal_error(error):
        """Catch 500 errors"""
        return make_response(jsonify({
            "Message": "Internal server"
        }), 200)

    return app
