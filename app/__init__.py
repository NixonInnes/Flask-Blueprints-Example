from flask import Flask
from flask.ext.bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy

from config import config

bootstrap = Bootstrap()
db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    bootstrap.init_app(app)
    db.init_app(app)

    if not app.debug and not app.testing:
        from flask.ext.sslify import SSLify
        sslify = SSLify(app)

    from app.blueprints.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # Add additional blueprints here...
    # example:
    # from app.blueprints.myblueprint import myblueprint as myblueprint_blueprint
    # app.register_blueprint(myblueprint_blueprint, url_prefix='/myblueprint')

    return app
