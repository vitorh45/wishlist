from flask_restx import fields, Model, reqparse



client_query_args_parser = reqparse.RequestParser()
client_query_args_parser.add_argument(
    "email",
    type=str,
    location="args",
    required=True,
    nullable=False,
)

create_client_model = Model(
    "Create-Client",
    {
        "email": fields.String(
            example="john.wick@example.com",
            pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$",
            required=True,
        ),
        "name": fields.String(
            example="John Wick",
            pattern=r"[a-zA-Z]+",
            required=True,
        )
    }
)

client_response_model = Model(
    "ClientResponse",
    create_client_model)
client_response_model["id"] = fields.String(
                                        required=True,
                                        description="Client id",
                                        example="123e4567-e89b-12d3-a456-426614174000",
                                    )
client_response_model["insert_at"] = fields.DateTime(
                                            required=True,
                                            description="Client creation date",
                                            example="2022-01-01T00:00:00",
                                        )
client_response_model["update_at"] = fields.DateTime(
                                            required=True,
                                            description="Client creation date",
                                            example="2022-01-01T00:00:00",
                                        )


update_client_model = Model(
    "Updae-Client",
    {
        "name": fields.String(
            example="John Wick",
            pattern=r"[a-zA-Z]+",
            required=True,
        )
    }
)