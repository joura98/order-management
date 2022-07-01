from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config import config_map
db = SQLAlchemy()


def app_created(dev_class):
    app = Flask(__name__)
    config_class = config_map[dev_class]
    app.config.from_object(config_class)
    register_blueprint(app)
    CORS(app, resources={"/api/*": {"origins": "*"}})
    db.init_app(app)
    return app


def register_blueprint(app):
    from app.api import api
    app.register_blueprint(api)
