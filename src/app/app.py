import logging
import sys
from os import getenv

import json_logging
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from flask_redis import FlaskRedis


load_dotenv()

ENV = getenv("DEPLOY_ENV", default="Development")
redis = FlaskRedis()


def create_app(deploy_env: str = ENV) -> Flask:
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(f"app.config.{deploy_env}Config")

    _configure_logger(app=app)
    _register_blueprints(app=app)
    redis.init_app(app)

    return app


def _configure_logger(app: Flask) -> None:
    if not json_logging.ENABLE_JSON_LOGGING:
        json_logging.init_flask(enable_json=True)
        json_logging.init_request_instrument(app=app)

    logger = logging.getLogger("wishlist")
    logger.setLevel(app.config["LOGS_LEVEL"])

    if not logger.hasHandlers():
        logger.addHandler(logging.StreamHandler(sys.stdout))


def _register_blueprints(app: Flask) -> None:
    pass
