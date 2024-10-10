import json

from flask import Blueprint, request, Response, current_app
from flask_restx import Api, Resource, marshal
from flask_jwt_extended import jwt_required

from api.application.use_cases import (
    ClientsUseCase,
    ClientNotFound
)
from api.presentation.mappings import (
    CreateClientRequestMapping,
    UpdateClientRequestMapping
)
from api.presentation.schemas import (
    create_client_model,
    client_response_model,
    generic_response_model,
    client_query_args_parser,
    update_client_model
)

from .api import DOC, VERSION


blueprint = Blueprint("clients", __name__, url_prefix="/api/v1/clients")

api = Api(
    blueprint,
    version=VERSION,
    title="Wishlist Client API",
    description=f"{DOC} - Clients",
    doc="/docs/swagger"
)

ns = api.namespace("", description=DOC)
ns.add_model(create_client_model.name, create_client_model)
ns.add_model(client_response_model.name, client_response_model)
ns.add_model(generic_response_model.name, generic_response_model)


@ns.route("")
class Clients(Resource):
    @ns.expect(create_client_model, validate=True)
    @ns.response(201, "OK", client_response_model)
    @ns.response(400, "Bad Request", generic_response_model)
    @jwt_required()
    def post(self) -> tuple[dict, int]:
        mapping = CreateClientRequestMapping(payload=request.json)
        try:
            client = ClientsUseCase.create_client(data=mapping)
        except Exception as e:
            return {
                "code": "400",
                "message": str(e)
            }, 400

        return marshal(client, client_response_model), 201
    
    @ns.expect(client_query_args_parser)
    @ns.expect(update_client_model, validate=True)
    @ns.response(201, "OK", client_response_model)
    @ns.response(400, "Bad Request", generic_response_model)
    @jwt_required()
    def patch(self) -> tuple[dict, int]:
        query_args = client_query_args_parser.parse_args()
        mapping = UpdateClientRequestMapping(payload=request.json)
        try:
            client = ClientsUseCase.update_by_email(data=mapping, email=query_args["email"])
        except ClientNotFound as e:
            return {"message": str(e)}, 404
        except Exception as e:
            return {
                "code": "400",
                "message": str(e)
            }, 400

        return marshal(client, client_response_model), 200

    @ns.expect(client_query_args_parser)
    @ns.response(200, "OK", client_response_model)
    @ns.response(400, "Bad Request", generic_response_model)
    @ns.response(404, "Not found", generic_response_model)
    @jwt_required()
    def get(self) -> tuple[dict, int]:
        query_args = client_query_args_parser.parse_args()
        try:
            client = ClientsUseCase.get_by_email(email=query_args["email"])
        except ClientNotFound as e:
            return {"message": str(e)}, 404
        except Exception as e:
            return {
                "code": "400",
                "message": str(e)
            }, 400

        return marshal(client, client_response_model), 200

    @ns.expect(client_query_args_parser)
    @ns.response(200, "OK")
    @ns.response(400, "Bad Request", generic_response_model)
    @ns.response(404, "Not found", generic_response_model)
    @jwt_required()
    def delete(self) -> tuple[dict, int]:
        query_args = client_query_args_parser.parse_args()

        try:
            client = ClientsUseCase.delete_by_email(email=query_args["email"])
        except ClientNotFound as e:
            return {"message": str(e)}, 404
        except Exception as e:
            return {
                "code": "400",
                "message": str(e)
            }, 400
        return {}, 200