import datetime as dt

from flask_login import UserMixin, current_user
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash

from . import db


class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column("id", db.Integer, primary_key=True)
    user = db.Column("user", db.Unicode, unique=True)
    password = db.Column("password", db.Unicode)
    email = db.Column("email", db.Unicode)
    name = db.Column("name", db.Unicode)
    cpf = db.Column("cpf", db.Unicode)
    admin = db.Column("admin", db.Boolean)

    @staticmethod
    def create(user: str, password: str, email: str, cpf: str, admin=False):
        hash_passwd = generate_password_hash(password)
        user = User(user=user, password=hash_passwd, email=email, cpf=cpf, admin=admin)
        db.session.add(user)
        db.session.commit()

        return user

    @staticmethod
    def get(**kwargs):
        return User.query.filter_by(**kwargs).first()

    def update(self):
        pass

    @staticmethod
    def delete(**kwargs):
        User.query.filter_by(**kwargs).delete()
        db.session.commit()

    @property
    def is_admin(self):
        return self.admin


class Estoque(db.Model):
    __tablename__ = "estoque"
    balance = db.relationship("Balance", backref="balance", lazy="dynamic")

    id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column("name", db.Unicode)
    price = db.Column("price", db.Float)
    unity = db.Column("unity", db.Unicode)
    avaliable = db.Column("avaliable", db.Boolean)
    amount = db.Column("amount", db.Integer)

    @staticmethod
    def get_balance(id: int):
        balance = Balance.query.filter_by(item_id=id)
        entry = sum([i.quant for i in balance.filter_by(event="Entrada")])
        sale = sum([i.quant for i in balance.filter_by(event="Saida")])

        return entry - sale

    def __str__(self):
        return self.name

    @staticmethod
    def get_item_details(id: int):
        item = Estoque.query.get(id)
        return {"name": item.name, "price": item.price, "unity": item.unity}

    def to_dict(self) -> dict:
        return dict((col, getattr(self, col)) for col in self.__table__.columns.keys())

    @property
    def details(self):
        details = self.to_dict()
        details.pop("avaliable")
        return details

    @staticmethod
    def get_avaliable_items():
        return Estoque.query.filter_by(avaliable=True)


class Balance(db.Model):
    __tablename__ = "balance"
    id = db.Column("id", db.Integer, primary_key=True)
    item_id = db.Column("item_id", db.Integer, db.ForeignKey("estoque.id"))
    quant = db.Column("quant", db.Integer)
    date = db.Column("date", db.Date, default=dt.datetime.now())
    event = db.Column("event", db.Unicode)


class Order(db.Model):
    __tablename__ = "order"
    id = db.Column("id", db.Integer, primary_key=True)
    employee_id = db.Column("employee_id", db.Integer, db.ForeignKey("user.id"))
    register_id = db.Column("register_id", db.Integer, db.ForeignKey("register.id"))
    type_pgto = db.Column("type_pgto", db.Integer)
    type_of_sale = db.Column("type_of_sale", db.Integer)
    date = db.Column("date", db.Date, default=dt.datetime.utcnow())
    freight = db.Column("freight", db.Float, default=0.00)
    discount = db.Column("discount", db.Float, default=0.00)
    is_finished = db.Column("is_finished", db.Boolean, default=False)

    user = db.relationship("User", foreign_keys=employee_id)
    register = db.relationship("Register", foreign_keys=register_id)

    def get_total_amount(self) -> float:
        return (
            sum([i.estoque.price * i.amount for i in self.get_details()])
            + self.freight
            - self.discount
        )

    @property
    def details(self):
        detail = self.to_dict()
        detail.pop("employee_id")
        detail.pop("register_id")
        detail["date"] = str(self.date)
        detail.update(
            {
                "employee": {"id": self.employee_id, "name": self.user.name},
                "register": self.register.details,
                "description": [i.details for i in self.get_details()],
            }
        )

        return detail

    @staticmethod
    def get_current_user_order():
        order = Order.query.filter_by(
            employee_id=current_user.id, is_finished=False
        ).first()

        if order is None:
            order = Order()
            order.employee_id = current_user.id
            order.save()

        return order

    @staticmethod
    def get(id: int):
        return Order.query.filter_by(id=id).first()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def add_item(self, item_id: int, amount: int) -> dict:
        item = DescOrder(order_id=self.id, product_id=item_id, amount=amount)
        item.save()
        item_detail = {
            "item_id": item.product_id,
            "name": item.estoque.name,
            "amount": item.amount,
            "price": item.estoque.price,
        }

        return item_detail

    def add_item_by_form(self, form) -> dict:
        item = DescOrder()
        form.populate_obj(item)
        item.order_id = self.id

        return item.save()

    def get_details(self):
        return DescOrder.query.filter_by(order_id=self.id).all()

    def finish(self):
        self.is_finished = True
        self.save()

    @property
    def item_count(self):
        return len(DescOrder.query.filter_by(order_id=self.id).all())

    @staticmethod
    def remove_item(item_id: int) -> dict:
        item = DescOrder.query.filter_by(id=item_id).first()

        if item is not None:
            item.remove()
            response = {"success": True, "message": "Item excluido com sucesso!"}

        else:
            response = {
                "success": False,
                "message": f"Não foi possível localizar o item com o ID {item_id}",
            }

        return response

    @property
    def payment_type(self):
        payment = PaymentType.get(self.type_pgto)

        if payment is not None:
            return payment.type_of_payment

        else:
            return ""

    @property
    def sale_type(self):
        sale = SaleType.get(self.type_pgto)

        if sale is not None:
            return sale.type_of_sale

        else:
            return ""

    def to_dict(self):
        return dict((col, getattr(self, col)) for col in self.__table__.columns.keys())


class DescOrder(db.Model):
    __tablename__ = "desc_order"
    id = db.Column("id", db.Integer, primary_key=True)
    order_id = db.Column("order_id", db.Integer, db.ForeignKey("order.id"))
    product_id = db.Column("product_id", db.Integer, db.ForeignKey("estoque.id"))
    amount = db.Column("amount", db.Integer)

    order = db.relationship("Order", foreign_keys=order_id)
    estoque = db.relationship("Estoque", foreign_keys=product_id)

    def save(self) -> dict:
        try:
            db.session.add(self)
            db.session.commit()

        except IntegrityError:
            db.session.rollback()
            response = {
                "success": False,
                "message": "Não foi possível adicionar o item",
            }

        else:
            response = {"success": True, "message": "Item criado com sucesso"}

        return response

    def remove(self):
        db.session.delete(self)
        db.session.commit()

    def to_dict(self):
        return dict((col, getattr(self, col)) for col in self.__table__.columns.keys())

    @property
    def details(self) -> dict:
        detail = self.estoque.details
        detail.update(
            {"id": self.id, "item_id": self.estoque.id, "amount": self.amount}
        )

        return detail


class Register(db.Model):
    __tablename__ = "register"
    id = db.Column("id", db.Integer, primary_key=True)
    zip = db.Column("zip", db.Integer)
    city = db.Column("city", db.Unicode)
    address = db.Column("address", db.Unicode)
    district = db.Column("district", db.Unicode)
    type = db.Column("type", db.Unicode)

    @staticmethod
    def get(id):
        return Register.query.filter_by(id=id).first()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def to_dict(self):
        return dict((col, getattr(self, col)) for col in self.__table__.columns.keys())

    def remove(self):
        db.session.delete(self)
        db.session.commit()

    @property
    def details(self):
        address = self.to_dict()
        if self.type == "cliente":
            cliente = Cliente.query.filter_by(register_id=self.id).first()
            address.update({"cliente": cliente.details if cliente is not None else {}})

        elif self.type == "financeiro":
            financeiro = Financeiro.query.filter_by(register_id=self.id).first()
            address.update(
                {
                    "financeiro": financeiro.to_dict()
                    if financeiro is not None
                    else {}
                }
            )

        return address

    def __repr__(self):
        if self.type == "financeiro":
            return Financeiro.query.filter_by(register_id=self.id).first().name.capitalize()

        elif self.type == "cliente":
            return Cliente.query.filter_by(register_id=self.id).first().name.capitalize()


class Cliente(db.Model):
    __tablename__ = "cliente"
    id = db.Column("id", db.Integer, primary_key=True)
    register_id = db.Column("register_id", db.Integer, db.ForeignKey("register.id"))
    name = db.Column("name", db.Unicode)
    cel = db.Column("cel", db.Integer)
    phone = db.Column("phone", db.Integer)
    aniversario = db.Column("aniversario", db.Unicode)
    observacao = db.Column("observacao", db.Unicode)

    register = db.relationship("Register", foreign_keys=register_id)


    @staticmethod
    def create_by_form(form):
        cliente = Cliente()
        register = Register()

        form.populate_obj(register)
        register.type = "cliente"
        register.save()

        form.populate_obj(cliente)
        cliente.register_id = register.id

        response = cliente.save()

        if not response["success"]:
            register.delete()

        return response

    def update_by_form(self, form):
        form.populate_obj(self)
        form.populate_obj(self.register)
        self.register.save()
        response = self.save()

        return response

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()

        except IntegrityError:
            db.session.rollback()
            response = {
                "success": False,
                "message": "Já existe um cadastro com o mesmo CPF, RG ou CRM no banco de dados.",
            }

        else:
            response = {
                "success": True,
                "message": "Cliente cadastrado com successo!",
                "object": self,
            }

        return response

    @staticmethod
    def get_all():
        return Cliente.query.all()

    @staticmethod
    def get(id: int):
        return Cliente.query.filter_by(id=id).first()

    @staticmethod
    def get_aniversariantes(mes: int):
        lista = [item for item in Cliente.query.all() if item.aniversario[3:5]==mes["mes"]]
        return lista


    def remove(self):
        self.register.remove()

        db.session.delete(self)
        db.session.commit()
        response = {"success": True, "message": "Registro excluido com sucesso!"}

        return response

    def to_dict(self) -> dict:
        return dict((col, getattr(self, col)) for col in self.__table__.columns.keys())

    @property
    def details(self) -> dict:
        details = self.to_dict()
        details.pop("register_id")
        return details


class Financeiro(db.Model):
    __tablename__ = "financeiro"
    id = db.Column("id", db.Integer, primary_key=True)
    register_id = db.Column("register_id", db.Integer, db.ForeignKey("register.id"))
    name = db.Column("name", db.Unicode)
    cnpj = db.Column("cnpj", db.Integer)
    adm_name = db.Column("adm_name", db.Unicode)
    adm_email = db.Column("adm_email", db.Unicode)
    adm_cel = db.Column("adm_cel", db.Integer)
    adm_phone = db.Column("adm_phone", db.Integer)
    enf_name = db.Column("enf_name", db.Unicode)
    enf_email = db.Column("enf_email", db.Unicode)
    enf_cel = db.Column("enf_cel", db.Integer)
    enf_phone = db.Column("enf_phone", db.Integer)

    register = db.relationship("Register", foreign_keys=register_id)

    @staticmethod
    def get_all():
        return Financeiro.query.all()

    @staticmethod
    def get(id: int):
        return Financeiro.query.filter_by(id=id).first()

    def save(self):
        db.session.add(self)
        db.session.commit()
        response = {"success": True, "message": "Instituiçao cadastrada com successo!"}

        return response

    @staticmethod
    def create_by_form(form):
        financeiro = Financeiro()
        register = Register()

        form.populate_obj(register)
        register.type = "financeiro"
        register.save()

        form.populate_obj(financeiro)
        financeiro.register_id = register.id

        response = financeiro.save()

        if not response["success"]:
            register.delete()

        return response

    def update_by_form(self, form):
        form.populate_obj(self)
        form.populate_obj(self.register)
        self.register.save()
        response = self.save()

        return response

    def remove(self) -> dict:
        self.register.remove()
        db.session.delete(self)
        db.session.commit()
        response = {"success": True, "message": "Registro excluido com sucesso!"}

        return response

    def to_dict(self):
        return dict((col, getattr(self, col)) for col in self.__table__.columns.keys())


class Speciality(db.Model):
    __tablename__ = "speciality"
    id = db.Column("id", db.Integer, primary_key=True)
    speciality = db.Column("speciality", db.Unicode)


class SaleType(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    type_of_sale = db.Column("type_of_sale", db.Unicode)

    @staticmethod
    def get(id: int):
        return SaleType.query.filter_by(id=id).first()


class PaymentType(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    type_of_payment = db.Column("type_of_payment", db.Unicode)

    @staticmethod
    def get(id: int):
        return PaymentType.query.filter_by(id=id).first()
