import json

from flask import Blueprint, request, Response, current_app
from flask_restx import Api, Resource, marshal
from flask_jwt_extended import jwt_required

from api.application.use_cases import (
    ClientNotFound,
    WishlistUseCase,
    WishlistAlreadyExists,
    WishlistNotFound,
    WishlistAlreadyContainsThisProduct
)
from api.presentation.mappings import (
    CreateWishlistRequestMapping,
    AddProductWishlistRequestMapping
)
from api.presentation.schemas import (
    create_wishlist_model,
    wishlist_response_model,
    wishlist_add_product_model,
    generic_response_model
)


VERSION = "0.0.1"
DOC = "Wishlist API"

blueprint = Blueprint("wishlist", __name__, url_prefix="/api/v1/wishlists")

api = Api(
    blueprint,
    version=VERSION,
    title="Wishlist API",
    description=f"{DOC} - Wishlist",
    doc="/docs/swagger"
)

ns = api.namespace("", description=DOC)


@ns.route("")
class Wishlists(Resource):
    @ns.expect(create_wishlist_model, validate=True)
    @ns.response(201, "OK", wishlist_response_model)
    @ns.response(400, "Bad Request", generic_response_model)
    @jwt_required()
    def post(self) -> tuple[dict, int]:
        mapping = CreateWishlistRequestMapping(payload=request.json)
        try:
            wishlist = WishlistUseCase.create_wishlist(data=mapping)
        except ClientNotFound as e:
            return {"message": str(e)}, 404
        except WishlistAlreadyExists as e:
            return {"message": str(e)}, 409
        except Exception as e:
            return {
                "code": "400",
                "message": str(e)
            }, 400

        return marshal(wishlist, wishlist_response_model), 201


@ns.route("/<uuid:wishlist_id>")
class WishlistDetail(Resource):
    @ns.response(201, "OK", wishlist_response_model)
    @ns.response(400, "Bad Request", generic_response_model)
    @jwt_required()
    def get(self, wishlist_id) -> tuple[dict, int]:
        try:
            wishlist = WishlistUseCase.get_by_id(wishlist_id=wishlist_id)
        except WishlistNotFound as e:
            return {"message": str(e)}, 404
        except Exception as e:
            return {
                "code": "400",
                "message": str(e)
            }, 400

        return marshal(wishlist, wishlist_response_model), 200
    
    @ns.expect(wishlist_add_product_model, validate=True)
    @ns.response(200, "OK", wishlist_response_model)
    @ns.response(400, "Bad Request", generic_response_model)
    @jwt_required()
    def put(self, wishlist_id) -> tuple[dict, int]:
        mapping = AddProductWishlistRequestMapping(payload=request.json)
        try:
            wishlist = WishlistUseCase.add_product(wishlist_id=wishlist_id, data=mapping)
        except WishlistAlreadyContainsThisProduct as e:
            return {
                "code": "400",
                "message": str(e)
            }, 400
        except Exception as e:
            return {
                "code": "400",
                "message": str(e)
            }, 400

        return marshal(wishlist, wishlist_response_model), 200
