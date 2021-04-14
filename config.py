import os
import logging
from logging.handlers import RotatingFileHandler
from flask import has_request_context, request
from flask.logging import default_handler

basedir = os.path.abspath(os.path.dirname(__file__))

class RequestFormatter(logging.Formatter):
    def format(self, record):
        if has_request_context():
            record.url = request.url
            record.remote_addr = request.remote_addr
        else:
            record.url = None
            record.remote_addr = None

        return super().format(record)

default_formatter = RequestFormatter(
    '[%(asctime)s] %(remote_addr)s requested %(url)s\n'
    '%(levelname)s in %(module)s: %(message)s'
)
default_handler.setFormatter(default_formatter)

log_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")


def gen_uuid():
    import uuid
    return str(uuid.uuid4())


class Config(object):
    SECRET_KEY = os.getenv('SECRET_KEY', gen_uuid())
    APP_NAME = os.getenv('APP_NAME', 'NixFlask')

    LOG_DIR = os.path.join(basedir, 'logs')
    LOG_LEVEL= os.getenv("LOG_LEVEL", "DEBUG")

    @classmethod
    def make_log_folders(cls):
        if not os.path.exists(cls.LOG_DIR):
            os.makedirs(cls.LOG_DIR)

    @classmethod
    def init_app(cls, app):
        cls.make_log_folders()
        log_handler = RotatingFileHandler(
            os.path.join(cls.LOG_DIR, cls.APP_NAME+'.log'),
            maxBytes=10000,
            backupCount=3)
        log_handler.setLevel(cls.LOG_LEVEL)
        log_handler.setFormatter(log_formatter)
        app.logger.setLevel(cls.LOG_LEVEL)
        app.logger.addHandler(log_handler)


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DEV_DATABASE_URI',
        'sqlite:///' + os.path.join(basedir, 'dev-db.sqlite'))
    LOG_DIR = os.path.join(Config.LOG_DIR, 'dev')
    LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")



class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URI',
        'sqlite:///' + os.path.join(basedir, 'test-db.sqlite'))
    LOG_DIR = os.path.join(Config.LOG_DIR, 'test')
    LOG_LEVEL = os.getenv("LOG_LEVEL", "WARN")



class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI',
        'sqlite:///' + os.path.join(basedir, 'db.sqlite'))
    LOG_LEVEL = os.getenv("LOG_LEVEL", "ERROR")



config = {
    'development': DevConfig,
    'testing':     TestConfig,
    'production':  ProdConfig,
    'default':     DevConfig
}
