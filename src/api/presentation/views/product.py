import json
from uuid import UUID

from flask import Blueprint, request, Response, current_app
from flask_restx import Api, Resource, marshal
from flask_jwt_extended import jwt_required


from api.application.use_cases import (
    ProductUseCase,
    ProductNotFound
)
from api.presentation.schemas import (
    product_response_model,
    generic_response_model,
    product_query_args_parser
)


VERSION = "0.0.1"
DOC = "Wishlist API"

blueprint = Blueprint("products", __name__, url_prefix="/api/v1/products")

api = Api(
    blueprint,
    version=VERSION,
    title="Wishlist Product API",
    description=f"{DOC} - Products",
    doc="/docs/swagger"
)

ns = api.namespace("", description=DOC)
ns.add_model(product_response_model.name, product_response_model)
ns.add_model(generic_response_model.name, generic_response_model)


@ns.route("")
class ProductsList(Resource):
    @ns.expect(product_query_args_parser)
    @ns.response(200, "OK", product_response_model)
    @ns.response(400, "Bad Request", generic_response_model)
    @ns.response(404, "Not found", generic_response_model)
    @jwt_required()
    def get(self) -> tuple[dict, int]:
        query_args = product_query_args_parser.parse_args()
        limit = query_args.get("limit", 20)
        offset = query_args.get("offset", 0)
        try:
            products = ProductUseCase.get_by_filters(limit=limit, offset=offset)
        except Exception as e:
            return {
                "code": "400",
                "message": str(e)
            }, 400
        return marshal(products,product_response_model), 200


@ns.route("/<string:product_id>")
class Product(Resource):
    @ns.response(200, "OK", product_response_model)
    @ns.response(400, "Bad Request", generic_response_model)
    @ns.response(404, "Not found", generic_response_model)
    @jwt_required()
    def get(self, product_id: UUID) -> tuple[dict, int]:
        try:
            product = ProductUseCase.get_by_id(product_id=product_id)
        except ProductNotFound as e:
            return {"message": str(e)}, 404
        except Exception as e:
            return {
                "code": "400",
                "message": str(e)
            }, 400

        return marshal(product, product_response_model), 200