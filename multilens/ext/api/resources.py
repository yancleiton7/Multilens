from flask_login import login_required
from flask_restful import Resource

from multilens.ext.db.models import Register, Cliente


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

        else:
            response = {}

        return response


class ResourceOrder(Resource):
    #@login_required
    def get_RO(self, id: int):
        #order = Order.get(id)
        if order is not None:
            response = order.details

        else:
            response = {}

        return response
