from flask_restx import fields, Model, reqparse
from .product import product_response_model

create_wishlist_model = Model(
    "Create-Wishlist",
    {
        "client_id": fields.String(
            example="123e4567-e89b-12d3-a456-426614174000",
            required=True,
        ),
    }
)

wishlist_response_model = Model(
    "WishlistResponse",
    create_wishlist_model)
wishlist_response_model["id"] = fields.String(
                                        required=True,
                                        description="Wishlist id",
                                        example="123e4567-e89b-12d3-a456-426614174000",
                                    )
wishlist_response_model["insert_at"] = fields.DateTime(
                                            required=True,
                                            description="Client creation date",
                                            example="2022-01-01T00:00:00",
                                        )
wishlist_response_model["update_at"] = fields.DateTime(
                                            required=True,
                                            description="Client creation date",
                                            example="2022-01-01T00:00:00",
                                        )

wishlist_response_model["products"] = fields.List(
                                        fields.Nested(product_response_model),
                                        description="List of products",
                                        required=True,
                                        example=[{}, {}]
                                    )

wishlist_add_product_model = Model(
    "Wishlist-Add-Product",
    {
        "product_id": fields.String(
            example="123e4567-e89b-12d3-a456-426614174000",
            required=True,
        ),
    }
)