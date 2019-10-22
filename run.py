import os
from flask_cors import CORS
from flask_restful import Api
from flask_jwt_extended import JWTManager,exceptions
from api import create_app
from api.configs.routes import register_routes
from api.util.blacklist_helpers import is_token_revoked
from api.configs.flask_config import config_by_name
import logging
# from logging.handlers import RotatingFileHandler


app = create_app()
CORS(app)
api = Api(app)
jwt = JWTManager(app)

# This method will check if a token is blacklisted, 
# and will be called automatically when blacklist is enabled
@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return is_token_revoked(decrypted_token)


register_routes(api)


logger = logging.getLogger('werkzeug')
handler = logging.FileHandler('access.log')
logger.addHandler(handler)
app.logger.error('first test message...')
logger.error('first test message...')

if __name__ == '__main__':
    app.run(debug=True)
