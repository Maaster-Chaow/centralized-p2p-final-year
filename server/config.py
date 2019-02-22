import os


_cwd = os.path.abspath(os.path.dirname(__file__))
_dev_db_dir = os.path.join(_cwd, '../test/server/test.db')

ADMINS_EMAIL = ['kyunkiimgood@gmail.com']


class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'apple'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + _dev_db_dir


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    SECRET_KEY = os.getenv('SECRET_KEY')
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')



class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


app_config = dict(
    production=ProductionConfig,
    development=DevelopmentConfig,
    testing=TestingConfig)