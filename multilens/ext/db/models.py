import datetime as dt
from datetime import datetime

from flask_login import UserMixin, current_user
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash

from . import db

db.metadata.clear()

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
    #balance = db.relationship("Balance", backref="balance", lazy="dynamic")

    id = db.Column("id", db.Integer, primary_key=True)
    nome_produto = db.Column("nome_produto", db.Unicode)
    valor_pago = db.Column("valor_pago", db.Float)
    quantidade = db.Column("quantidade", db.Integer)
    data_compra = db.Column("data_compra", db.Boolean)
    observacao = db.Column("observacao", db.Integer)


    @staticmethod
    def get_avaliable_items():
        return Estoque.query.all()

    @staticmethod
    def get(id: int):
        return Estoque.query.filter_by(id=id).first()
    


    @staticmethod
    def get_balance(id: int):
        balance = Balance.query.filter_by(item_id=id)
        entry = sum([i.quantidade for i in balance.filter_by(event="Entrada")])
        sale = sum([i.quantidade for i in balance.filter_by(event="Saida")])

        return entry - sale

class Produto(db.Model):
    __tablename__ = "produtos"
    balance = db.relationship("Balance", backref="balance", lazy="dynamic")

    id = db.Column("id", db.Integer, primary_key=True)
    data_cadastro = db.Column("data_cadastro", db.Unicode, default=dt.datetime.now().strftime("%m/%d/%Y"))
    nome_produto = db.Column("nome_produto", db.Unicode)
    grupo = db.Column("grupo", db.Unicode)
    tipo = db.Column("tipo", db.Unicode)
    observacao = db.Column("observacao", db.Unicode)
    estoque_minimo = db.Column("estoque_minimo", db.Unicode)
    unidade = db.Column("unidade", db.Unicode)

    @staticmethod
    def necessita_compra(id: int):
        if Produto.get_minimo(id)<Produto.get_balance(id):
            return False
        else:
            return True

    @staticmethod
    def get_preco(id: int):
        balance = Balance.query.filter_by(item_id=id)
        preco = [i.preco for i in balance.filter_by(event="Entrada")]
        if len(preco)>1:
            preco = preco[-1:]
            preco = "R$ "+str(preco[0])
        elif len(preco)==1:
            preco = "R$ "+str(preco[0])
        else:
            preco = "Nenhuma entrada cadastrada"
        
        return preco

    @staticmethod
    def get_minimo(id: int):
        produto = Produto.query.filter_by(id=id).first()
        return produto.estoque_minimo
    
    @staticmethod
    def get_balance(id: int):
        balance = Balance.query.filter_by(item_id=id)
        entry = sum([i.quantidade for i in balance.filter_by(event="Entrada")])
        sale = sum([i.quantidade for i in balance.filter_by(event="Saida")])

        return entry - sale

    @staticmethod
    def get_tipo(id: int):
        produto = Produto.query.filter_by(id=id).first()
        tipo = Tipo.get(produto.tipo).tipo
        return tipo
    @staticmethod
    def get_grupo(id: int):
        produto = Produto.query.filter_by(id=id).first()
        grupo = Grupo.get(produto.grupo).grupo
        return grupo

    @staticmethod
    def get_id(nome_produto: str):
        produto = Produto.query.filter_by(nome_produto=nome_produto).first()
        id = produto.id
        return id
    @staticmethod
    def get(id: int):
        return Produto.query.filter_by(id=id).first()

    @staticmethod
    def create_by_form(form):
        produto = Produto()
        form.populate_obj(produto)
        response = produto.save()
        return response

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()

        except:
            db.session.rollback()
            response = {
                "success": False,
                "message": "Aconteceu algo errado, por favor tente novamente",
            }

        else:
            response = {
                "success": True,
                "message": "Produto cadastrado com successo!",
                "object": self,
            }

        return response
    
    def update_by_form(self, form):
        form.populate_obj(self)
        response = self.save()
        response["message"] = "Produto editado com successo!"

        return response
    
    def remove(self):
        db.session.delete(self)
        db.session.commit()
        response = {"success": True, "message": "Produto excluido com sucesso!"}

        return response
    
    @staticmethod
    def get_all():
        return Produto.query.all()

class Pedidos(db.Model):
    __tablename__ = "pedidos"
    id = db.Column("id", db.Integer, primary_key=True)
    pedido = db.Column("pedido", db.Unicode)
    data_pedido = db.Column("data_pedido", db.Unicode)
    data_entrega = db.Column("data_pedido", db.Unicode)
    hora_entrega = db.Column("hora_entrega", db.Unicode)
    quantidade = db.Column("quantidade", db.Integer)
    id_cliente = db.Column("id_cliente", db.Integer)
    tipo_retirada = db.Column("tipo_retirada", db.Integer)
    tipo_pagamento = db.Column("tipo_pagamento", db.Integer)
    endereco_entrega = db.Column("endereco_entrega", db.Unicode)
    observacao = db.Column("observacao", db.Unicode)
    status_pagamento = db.Column("status_pagamento", db.Unicode)     





class Balance(db.Model):
    __tablename__ = "balance"
    id = db.Column("id", db.Integer, primary_key=True)
    item_id = db.Column("item_id", db.Integer, db.ForeignKey("produtos.id"))
    quantidade = db.Column("quantidade", db.Integer)
    date = db.Column("date", db.Unicode)
    event = db.Column("event", db.Unicode)
    preco = db.Column("preco", db.Unicode, default="00,00")
    observacao = db.Column("observacao", db.Unicode)

    

    @staticmethod
    def get(id: int):
        return Balance.query.filter_by(id=id).first()

    @staticmethod
    def create_by_form(form):
        balance = Balance()
        form.populate_obj(balance)
        response = balance.save()
        return response

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()

        except:
            db.session.rollback()
            response = {
                "success": False,
                "message": "Aconteceu algo errado, por favor tente novamente",
            }

        else:
            response = {
                "success": True,
                "message": "Produto cadastrado com successo!",
                "object": self,
            }

        return response
    
    def update_by_form(self, form):
        form.populate_obj(self)
        response = self.save()
        response["message"] = "Produto editado com successo!"

        return response
    
    def remove(self):
        db.session.delete(self)
        db.session.commit()
        response = {"success": True, "message": "Produto excluido com sucesso!"}

        return response
    
    @staticmethod
    def get_all():
        return Balance.query.all()

class Tipo(db.Model):
    __tablename__ = "tipo"
    id = db.Column("id", db.Integer, primary_key=True)
    tipo = db.Column("tipo", db.Unicode)

    @staticmethod
    def get(id: int):
        return Tipo.query.filter_by(id=id).first()

class Grupo(db.Model):
    __tablename__ = "grupo"
    id = db.Column("id", db.Integer, primary_key=True)
    grupo = db.Column("grupo", db.Unicode)

    @staticmethod
    def get(id: int):
        return Grupo.query.filter_by(id=id).first()

class Retirada(db.Model):
    __tablename__ = "retirada"
    id = db.Column("id", db.Integer, primary_key=True)
    tipo_retirada = db.Column("tipo_retirada", db.Unicode)

    @staticmethod
    def get(id: int):
        return Retirada.query.filter_by(id=id).first()

class Pagamento(db.Model):
    __tablename__ = "pagamento"
    id = db.Column("id", db.Integer, primary_key=True)
    tipo_pagamento = db.Column("tipo_pagamento", db.Unicode)

    @staticmethod
    def get(id: int):
        return Pagamento.query.filter_by(id=id).first()

class Financeiro(db.Model):
    __tablename__ = "institution"
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
        return Institution.query.all()

    @staticmethod
    def get(id: int):
        return Institution.query.filter_by(id=id).first()

    def save(self):
        db.session.add(self)
        db.session.commit()
        response = {"success": True, "message": "Instituiçao cadastrada com successo!"}

        return response

    @staticmethod
    def create_by_form(form):
        institution = Institution()
        register = Register()

        form.populate_obj(register)
        register.type = "institution"
        register.save()

        form.populate_obj(institution)
        institution.register_id = register.id

        response = institution.save()

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

        elif self.type == "institution":
            institution = Institution.query.filter_by(register_id=self.id).first()
            address.update(
                {
                    "institution": institution.to_dict()
                    if institution is not None
                    else {}
                }
            )

        return address

    def __repr__(self):
        if self.type == "institution":
            return Institution.query.filter_by(register_id=self.id).first().name.capitalize()

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
