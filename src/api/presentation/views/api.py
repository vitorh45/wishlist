from werkzeug.exceptions import Unauthorized
from flask import Blueprint, request
from flask_restx import Api, Resource

from api.presentation.schemas import (
    index_model,
    login_model,
    login_response_model,
    create_client_model,
    client_response_model,
    generic_response_model,
    client_query_args_parser,
    update_client_model,
    product_response_model,
    product_query_args_parser,
    create_wishlist_model,
    wishlist_response_model,
    wishlist_add_product_model,
)
from .user import UserLogin
from .client import Clients
from .product import ProductsList, Product
from .wishlist import Wishlists, WishlistDetail

VERSION = "0.0.1"
DOC = "Wishlist API"

blueprint = Blueprint("index", __name__)

api = Api(
    blueprint,
    version=VERSION,
    title="Wishlist API",
    description=f"{DOC} - Index",
    doc="/docs/swagger"
)

ns = api.namespace("", description=DOC)

ns.add_model(index_model.name, index_model)
ns.add_model(login_model.name, login_model)
ns.add_model(login_response_model.name, login_response_model)
ns.add_model(create_client_model.name, create_client_model)
ns.add_model(client_response_model.name, client_response_model)
ns.add_model(generic_response_model.name, generic_response_model)
ns.add_model(update_client_model.name, update_client_model)
ns.add_model(product_response_model.name, product_response_model)
ns.add_model(create_wishlist_model.name, create_wishlist_model)
ns.add_model(wishlist_response_model.name, wishlist_response_model)
ns.add_model(wishlist_add_product_model.name, wishlist_add_product_model)


ns.add_resource(UserLogin, "/api/v1/user/login")
ns.add_resource(Clients, "/api/v1/clients")
ns.add_resource(ProductsList, "/api/v1/products")
ns.add_resource(Product, "/api/v1/products/<product_id>")
ns.add_resource(Wishlists, "/api/v1/wishlists")
ns.add_resource(WishlistDetail, "/api/v1/wishlists/<wishlist_id>")

@ns.route("/health-status")
class Index(Resource):
    @ns.response(200, "OK", index_model)
    def get(self) -> tuple[dict, int]:
        return dict(
            service=DOC,
            version=VERSION
        ), 200
