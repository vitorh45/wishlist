from werkzeug.exceptions import Unauthorized
from flask import Blueprint, request
from flask_restx import Api, Resource

from api.presentation.mappings import (
    UserLoginRequestMapping
)

from api.application.use_cases import UserUseCase, LoginNotAuthorized

from api.presentation.schemas import (
    login_model,
    login_response_model
)


VERSION = "0.0.1"
DOC = "Wishlist API"

blueprint = Blueprint("user", __name__, url_prefix="/api/v1/user")

api = Api(
    blueprint,
    version=VERSION,
    title="Wishlist API",
    description=f"{DOC} - User",
    doc="/docs/swagger"
)

ns = api.namespace("", description=DOC)

ns.add_model(login_model.name, login_model)
ns.add_model(login_response_model.name, login_response_model)


@ns.route("/login")
class UserLogin(Resource):
    # @ns.expect(login_model, validate=True)
    @ns.response(200, "OK", login_response_model)
    def post(self) -> tuple[dict, int]:
        mapping = UserLoginRequestMapping(payload=request.json)
        try:
            token = UserUseCase.login(data=mapping)
        except LoginNotAuthorized as e:
            return {"message": str(e)}, 401

        return {"token": token}, 200