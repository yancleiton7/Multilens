from flask_restful import Api

from .resources import ResourceProdutos, ResourcePedido, ResourceRegister, ResourceCliente, ResourcePedidoItens, ResourceConta, ResourceParcelas

api = Api()


def init_app(app):
    api.add_resource(ResourceRegister, "/api/register/<int:id>")
    api.add_resource(ResourcePedido, "/api/pedido/<int:id>")
    api.add_resource(ResourceCliente, "/api/clientes/<int:id>")
    api.add_resource(ResourcePedidoItens, "/api/pedido_itens/<int:id>")
    api.add_resource(ResourceConta, "/api/contas/<int:id>")
    api.add_resource(ResourceParcelas, "/api/parcelas/<int:id>")
    api.add_resource(ResourceProdutos, "/api/produtos/<int:id>")
    api.init_app(app)
