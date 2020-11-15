from flask_login import login_required
from flask_restful import Resource

from multilens.ext.db.models import Register, Cliente, Pedidos, Pedido_item, Contas, Contas_parceladas


class ResourceCliente(Resource):
    #@login_required
    def get(self, id: int):
        cliente = Cliente.get(id)

        if cliente is not None:
            response = cliente.to_dict()
            #register = Register.get(response["register_id"]).to_dict()
            response["endereco"] = Register.get_endereco(response["register_id"])

        else:
            response = {}

        
        return response


class ResourceRegister(Resource):
    #@login_required
    def get(self, id: int):
        register = Register.get(id)
        if register is not None:
            response = register.to_dict()
            response["endereco"] = Register.get_endereco(response["register_id"])


        else:
            response = {}

        return response


class ResourcePedido(Resource):
    #@login_required
    def get(self, id: int):
        pedido = Pedidos.get(id)
        if pedido is not None:
            response = pedido.details
            for pedido_item in pedido.pedidos_itens:
                response[pedido_item.id] = pedido_item.produto
        else:
            response = {}

        return response

class ResourceConta(Resource):
    #@login_required
    def get(self, id: int):
        conta = Contas.get(id)
        if conta is not None:
            response = conta.details
            if response["tipo_mensalidade"] == "3":
                response["valor_parcelas"] = conta.parcelas_info.valor_parcelas
                response["parcelas_pagas"] = conta.parcelas_info.parcelas_pagas
                response["parcelas"] = conta.parcelas_info.parcelas



        else:
            response = {}

        return response

class ResourcePedidoItens(Resource):
    #@login_required
    def get(self, id: int):
        pedido_item = Pedido_item.get(id)
        if pedido_item is not None:
            response = pedido_item.details
        else:
            response = {}

        return response