import os
import sys
import datetime

# uncomment the line below for postgres database url from environment variable
# postgres_local_base = os.environ['DATABASE_URL']

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    DEBUG = True
    TESTING = False
    PROPAGATE_EXCEPTIONS = True # error handle
    FLASK_DEBUG=1 # Do not enable debug mode when deploying in production.
    SECRET_KEY = "B\xb2?.\xdf\x9f\xa7m\xf8\x8a%,\xf7\xc4\xfa\x91"
    # SECRET_KEY = os.environ.get("SECRET_KEY")
    # if not SECRET_KEY:
    #     raise ValueError("No SECRET_KEY set for Flask application")

    DB_NAME = "production-db"
    DB_USERNAME = "admin"
    DB_PASSWORD = "example"
    SESSION_COOKIE_SECURE = True
    TEMPLATES_AUTO_RELOAD = True
    JSON_SORT_KEYS = False

    JWT_SECRET_KEY = "B\xb2?.\xdf\x9f\xa7m\xf8\x8a%,\xf7\xc4\xfa\x91"
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS  = ['access', 'refresh']
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(seconds=360*60)
    JWT_IDENTITY_CLAIM = 'identity'

    # serve static file
    # By default Flask template_folder set to 'templates'
    # Flask configures the Jinja2 template engine automatically
        # app = Flask(__name__, template_folder= "templates")
    
    IMAGE_UPLOADS = "/static/images/uploads"
    STATIC_FOLDER = basedir.replace('configs','static')
    TEMPLATES_FOLDER = basedir.replace('configs','templates')
    if bool("win" in sys.platform):
        OS_WIN = True
    else:
        OS_WIN = False

class DevelopmentConfig(Config):
    DEBUG = True
    FLASK_DEBUG=1
    DB_CONNECTIONSTRING = "Driver={SQL Server};Server=10.0.0.60;UID=sa;PWD=@abc123@;Database=BIZMAN;"
    DB_SERVER = "10.0.0.60"
    DB_NAME = "BIZMAN"
    DB_USERNAME = "sa"
    DB_PASSWORD = "@abc123@"
    IMAGE_UPLOADS = "/static/images/uploads"
    SESSION_COOKIE_SECURE = False


class TestingConfig(Config):
   pass


class ProductionConfig(Config):
    DEBUG = False
    FLASK_DEBUG=0
    DB_CONNECTIONSTRING = "Driver={SQL Server};Server=10.0.0.60;UID=sa;PWD=@abc123@;Database=BIZMAN;"
    DB_SERVER = "10.0.0.60"
    DB_NAME = "BIZMAN"
    DB_USERNAME = "sa"
    DB_PASSWORD = "@abc123@"
    IMAGE_UPLOADS = "/static/images/uploads"
    SESSION_COOKIE_SECURE = False


config_by_name = dict(
    development=DevelopmentConfig,
    test=TestingConfig,
    production=ProductionConfig
)