import os
import logging
from logging.handlers import RotatingFileHandler

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.getenv('SECRET_KEY', 'somerandomkey')
    APP_NAME = os.getenv('APP_NAME', 'NixFlask')
    LOG_DIR = os.path.join(basedir, 'logs')

    @staticmethod
    def init_app(app):
        pass


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    DATABASE_URI = os.getenv('DEV_DATABASE_URI', \
        "sqlite:///{path}/{filename}".format(path=basedir, filename='dev-db.sqlite'))
    LOG_DIR = os.path.join(Config.LOG_DIR, 'dev')

    @classmethod
    def init_app(cls, app):
        super().init_app(app)
        log_handler = RotatingFileHandler(
            '{path}/{filename}.log'.format(path=cls.LOG_DIR, filename=cls.APP_NAME),
            maxBytes=10000,
            backupCount=3)
        log_handler.setLevel(logging.INFO)
        app.logger.addHandler(log_handler)


class TestConfig(Config):
    TESTING = True
    DATABASE_URI = os.getenv('TEST_DATABASE_URI', \
        "sqlite:///{path}/{filename}".format(path=basedir, filename='test-db.sqlite'))
    LOG_DIR = os.path.join(Config.LOG_DIR, 'test')

    @classmethod
    def init_app(cls, app):
        super().init_app(app)
        log_handler = RotatingFileHandler(
            '{path}/{filename}.log'.format(path=cls.LOG_DIR, filename=cls.APP_NAME),
            maxBytes=10000,
            backupCount=3)
        log_handler.setLevel(logging.WARN)
        app.logger.addHandler(log_handler)


class ProdConfig(Config):
    DATABASE_URI = os.getenv('DATABASE_URI', \
        "sqlite:///{path}/{filename}".format(path=basedir, filename='db.sqlite'))

    @classmethod
    def init_app(cls, app):
        super().init_app(app)
        log_handler = RotatingFileHandler(
            '{path}/{filename}.log'.format(path=cls.LOG_DIR, filename=cls.APP_NAME),
            maxBytes=10000,
            backupCount=3)
        log_handler.setLevel(logging.ERROR)
        app.logger.addHandler(log_handler)


config = {
    'development': DevConfig,
    'testing':     TestConfig,
    'production':  ProdConfig,
    'default':     DevConfig
}
