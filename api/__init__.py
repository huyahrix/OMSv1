import os
from flask import Flask,send_from_directory
from api.configs.flask_config import config_by_name

def create_app():
    app = Flask(__name__,
                static_url_path='', 
                static_folder='api/static',
                template_folder='api/templates')
    app.config.from_object(config_by_name[os.environ.get("FLASK_ENV", "development")])
    return app