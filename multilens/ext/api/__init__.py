from flask_restful import Api

from .resources import ResourceOrder, ResourceRegister

api = Api()


def init_app(app):
    api.add_resource(ResourceRegister, "/api/register/<int:id>")
    api.add_resource(ResourceOrder, "/api/order/<int:id>")

    api.init_app(app)
