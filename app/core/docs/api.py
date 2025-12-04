from flask_smorest import Api


def create_api(app):
    api = Api(
        app,
        spec_kwargs={
            "title": "Secure Auth API",
            "version": "1.0.0",
            "openapi_version": "3.0.3",
        },
    )
    return api
