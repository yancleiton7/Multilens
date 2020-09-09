from flask_login import login_required
from flask_restful import Resource

from multilens.ext.db.models import Order, Register


class ResourceRegister(Resource):
    @login_required
    def get(self, id: int):
        register = Register.get(id)

        if register is not None:
            response = register.to_dict()

        else:
            response = {}

        return response


class ResourceOrder(Resource):
    @login_required
    def get(self, id: int):
        order = Order.get(id)
        if order is not None:
            response = order.details

        else:
            response = {}

        return response
