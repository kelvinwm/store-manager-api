# instance/config.py
import os


class Config():
    DEBUG = False
    CSRF_ENABLED = True
    SECRET_KEY = os.getenv("SECRET_KEY")


class DevelopmentConfig(Config):
    '''Enable our debug mode to True in development in order to auto restart our server on code changes'''
    DEBUG = True


class TestingConfig(Config):
    '''Testing app configurations'''
    TESTING = True
    DEBUG = True


class ReleaseConfig(Config):
    '''Releasing app configurations'''
    DEBUG = False
    TESTING = False


app_configuration = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'release': ReleaseConfig,
}