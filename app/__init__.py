import os
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

from config import config

bootstrap = Bootstrap()
db = SQLAlchemy()
config = config[os.getenv('APP_CONFIG', 'default')]


def create_app():
    app = Flask(__name__)

    config.init_app(app)
    bootstrap.init_app(app)
    db.init_app(app)

    if not app.debug and not app.testing:
        try:
            from flask.ext.sslify import SSLify
            sslify = SSLify(app)
            app.logger.info('SSL enabled')
        except:
            pass

    from app.blueprints.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # Add additional blueprints here...
    # example:
    # from app.blueprints.myblueprint import myblueprint as myblueprint_blueprint
    # app.register_blueprint(myblueprint_blueprint, url_prefix='/myblueprint')

    return app
