import json
from os import getenv

import logging


class BaseConfig(object):
    DEBUG = False
    TESTING = False
    DEPLOY_ENV = getenv("DEPLOY_ENV", default="Development")
    LOGS_LEVEL = logging.INFO

   JWT_CACHE_EXPIRATION_SECONDS = getenv("JWT_CACHE_EXPIRATION_SECONDS")


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class TestingConfig(BaseConfig):
    DEBUG = True
    TESTING = True

    JWT_CACHE_EXPIRATION_SECONDS = 3600


class StagingConfig(BaseConfig):
    pass


class ProductionConfig(BaseConfig):
    LOGS_LEVEL = getenv("LOGS_LEVEL", default=logging.INFO)
