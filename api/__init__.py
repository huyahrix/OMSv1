import os
from flask import Flask
from api.configs.flask_config import config_by_name

def create_app():
    app = Flask(__name__)
    app.config.from_object(config_by_name[os.environ.get("FLASK_ENV", "development")])
    return app