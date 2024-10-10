import logging
from api.domain.models.user import User


logger = logging.getLogger("wishlist")


class LoginNotAuthorized(Exception):
    pass


class UserUseCase:
    @classmethod
    def login(cls, data: "PayloadMapping"):
        logger.info(
            "User login",
            extra={
                "props": {
                    "service": "UserLoginUseCase",
                    "service_method": "login",
                    "username": data.username
                }
            },
        )
        user = User.authenticate(
            username=data.username,
            password=data.password
        )
        if not user:
            raise LoginNotAuthorized(f"User not found")


        token = User.generate_access_token(
            username=data.username
        )

        return token