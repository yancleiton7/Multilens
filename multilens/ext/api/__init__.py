from flask_restful import Api

from .resources import ResourceOrder, ResourceRegister, ResourceCliente

api = Api()


def init_app(app):
    api.add_resource(ResourceRegister, "/api/register/<int:id>")
    api.add_resource(ResourceOrder, "/api/order/<int:id>")
    api.add_resource(ResourceCliente, "/api/clientes/<int:id>")
    api.init_app(app)
