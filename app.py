from extensions import app, api, db, jwt
from routes import UserBlueprint, StoreBlueprint, ItemBlueprint
import os
from blocklist import BLOCKLIST
from flask import jsonify
from datetime import timedelta


def create_app():
    # the configurations
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Store REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///student.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # initializing the instantiation imported from extensions.py file
    api.init_app(app)
    db.init_app(app)
    jwt.init_app(app)

    # the secret key configuration jwt
    app.config["JWT_SECRET_KEY"] = "overstuffed"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)

    # this is going to check the BLOCKLIST set if the token you're trying to use exist in the set
    # if the token is present in the set, it will return a 'token revoked' message
    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        return jwt_payload['jti'] in BLOCKLIST

    # this is going to be called when the access token expires
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({"message": "The Token has Expired.", "error": "token_expired"}), 401
        )

    # this is going to be called when the access token is invalid
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify({
                "description": "Signature verification failed.",
                "error": "invalid token"
            }), 401
        )

    # this is going to be called when you fail to provide an access token
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify({
                "description": "Request does not contain an access token.",
                "error": "authorization_required"
            }), 401
        )

    # registration of blueprints instantiation
    app.register_blueprint(UserBlueprint)
    app.register_blueprint(ItemBlueprint)
    app.register_blueprint(StoreBlueprint)

    """This creates the database for the project"""
    # @app.before_first_request
    # def create_tables():
    #     db.create_all()

    return app
