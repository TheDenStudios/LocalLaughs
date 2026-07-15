from flask import Flask

from .config import Config
from .database import init_database
from .routes import api


def create_app(config_object: type[Config] = Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_object)
    init_database(app)
    app.register_blueprint(api)
    return app
