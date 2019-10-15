import os
from flask_cors import CORS
from flask_restful import Api
from flask_jwt_extended import JWTManager,exceptions
from api import create_app
from api.configs.routes import register_routes
from api.util.blacklist import BLACKLIST
import logging

app = create_app()
CORS(app)
api = Api(app)
jwt = JWTManager(app)

# This method will check if a token is blacklisted, and will be called automatically when blacklist is enabled
@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token["jti"] in BLACKLIST


register_routes(api)

if __name__ == '__main__':
    app.run()


if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
