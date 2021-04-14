from flask import Flask
from flask_bootstrap import Bootstrap

from config import config

bootstrap = Bootstrap()



def create_app(config_name):
    app = Flask(__name__)

    Config = config[config_name]
    Config.init_app(app)

    app.config.from_object(Config)

    bootstrap.init_app(app)

    from .models import db
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
