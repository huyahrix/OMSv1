import os
from flask import Flask
from api.configs.config import config_by_name

def create_app():
    app = Flask(__name__)
    app.config.from_object(config_by_name[os.environ.get("FLASK_ENV", "development")])
    @app.route('/')
    def index():
        n = 1/0
        return "DIV/0 worked!"

    
    return app


# def index():
#     n = 1/0
#     return "DIV/0 worked!"