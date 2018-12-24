"""Configurations for server instances

1. Testing: used for running test cases.
2. Development: used using the phase of development.
3. Production: On deployment.
"""

import os


class Config():
    """Parent configuration class."""
    DEBUG = False
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')


class TestingConfig(Config):
    """Configurations for testing, with a separate test database."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://mchaow:123456@localhost/test_db'
    DEBUG = True

    
class DevelopmentConfig(Config):
    """Configuration for development."""
    DEBUG = True


class ProductionConfig(Config):
    """Configuration for production."""
    DEBUG = False
    TESTING = False


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    }
