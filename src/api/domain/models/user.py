import logging
from dataclasses import dataclass

from flask_jwt_extended import create_access_token
from flask import current_app


logger = logging.getLogger("wishlist")


@dataclass
class User:
    @classmethod
    def authenticate(
        cls,
        username: str,
        password: str
    ):
        
        logger.info(
            "User authenticate",
            extra={
                "props": {
                    "service": "User",
                    "service_method": "authenticate",
                    "username": username
                }
            },
        )

        if current_app.config.get("LOGIN_USERNAME") != username or current_app.config.get("LOGIN_PASSWORD") != password:
            return None

        return username
    
    @classmethod
    def generate_access_token(
        cls,
        username: str
    ):
        logger.info(
            "User generate_access_token",
            extra={
                "props": {
                    "service": "User",
                    "service_method": "generate_access_token",
                    "username": username
                }
            },
        )
        return create_access_token(identity=username)
