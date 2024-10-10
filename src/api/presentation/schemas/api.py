from flask_restx import fields, Model


index_model = Model(
    "Health-Status",
    {
        "service": fields.String(
            description="Service name"
        ),
        "version": fields.String(
            description="API version"
        )
    }
)


login_model = Model(
    "Login request",
    {
        "username": fields.String(
            description="Username"
        ),
        "password": fields.String(
            description="password"
        )
    }
)


login_response_model = Model(
    "Login response",
    {
        "token": fields.String(
            description="Token"
        )
    }
)


generic_response_model = Model(
    "GenericResponse",
    {
        "code": fields.String(example="ABC900"),
        "message": fields.String(example="Generic message")
    }
)

