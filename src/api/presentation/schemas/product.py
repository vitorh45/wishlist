from flask_restx import fields, Model, reqparse



product_query_args_parser = reqparse.RequestParser()
product_query_args_parser.add_argument(
    "limit",
    type=str,
    location="args",
    required=False,
    nullable=False,
)
product_query_args_parser.add_argument(
    "offset",
    type=str,
    location="args",
    required=False,
    nullable=False,
)

product_response_model = Model(
    "Product",
    {
        "id": fields.String(
            example="123e4567-e89b-12d3-a456-426614174000",
            required=True,
        ),
        "title": fields.String(
            example="Gibson Les Paul 69 cherry sunburst",
            pattern=r"[a-zA-Z]+",
            required=True,
        ),
        "brand": fields.String(
            example="Marshall",
            pattern=r"[a-zA-Z]+",
            required=True,
        ),
        "price": fields.Integer(
            example="120000",
            required=True,
        ),
        "image": fields.String(
            example="dir1/dir2/imagem.jpg",
            required=True,
        ),
        "insert_at": fields.DateTime(
            required=True,
            description="Product insert date",
            example="2022-01-01T00:00:00"
        ),
        "update_at": fields.DateTime(
            required=True,
            description="Product update date",
            example="2022-01-01T00:00:00"
        ),
    }
)