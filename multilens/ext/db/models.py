from flask_login import UserMixin
from werkzeug.security import generate_password_hash

from . import db


class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column("id", db.Integer, primary_key=True)
    user = db.Column("user", db.Unicode)
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


class Storage(db.Model):
    __tablename__ = "storage"
    id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column("name", db.Unicode)
    price = db.Column("price", db.Numeric)
    unity = db.Column("unity", db.Unicode)
    avaliable = db.Column("avaliable", db.Boolean)


class Balance(db.Model):
    __tablename__ = "balance"
    id = db.Column("id", db.Integer, primary_key=True)
    item_id = db.Column("item_id", db.Integer, db.ForeignKey("storage.id"))
    quant = db.Column("quant", db.Integer)
    date = db.Column("date", db.Date)
    event = db.Column("event", db.Unicode)

    storage = db.relationship("Storage", foreign_keys=item_id)


class Order(db.Model):
    __tablename__ = "order"
    id = db.Column("id", db.Integer, primary_key=True)
    employee_id = db.Column("employee_id", db.Integer, db.ForeignKey("user.id"))
    register_id = db.Column("register_id", db.Integer, db.ForeignKey("register.id"))
    date = db.Column("date", db.Date)
    type_pgto = db.Column("type_pgto", db.Unicode)
    type = db.Column("type", db.Unicode)

    user = db.relationship("User", foreign_keys=employee_id)
    register = db.relationship("Register", foreign_keys=register_id)


class DescOrder(db.Model):
    __tablename__ = "desc_order"
    id = db.Column("id", db.Integer, primary_key=True)
    order_id = db.Column("order_id", db.Integer, db.ForeignKey("order.id"))
    product_id = db.Column("product_id", db.Integer, db.ForeignKey("storage.id"))
    quant = db.Column("quant", db.Integer)
    unity_value = db.Column("unity_value", db.Integer)
    discount = db.Column("discount", db.Numeric)

    order = db.relationship("Order", foreign_keys=order_id)
    storage = db.relationship("Storage", foreign_keys=product_id)


class Register(db.Model):
    __tablename__ = "register"
    id = db.Column("id", db.Integer, primary_key=True)
    client_id = db.Column("client_id", db.Integer)
    institution_id = db.Column("institution_id", db.Integer)
    zip = db.Column("zip", db.Integer)
    country = db.Column("country", db.Unicode)
    address = db.Column("address", db.Unicode)
    type = db.Column("type", db.Unicode)


class Doctor(db.Model):
    __tablename__ = "doctor"
    register_id = db.Column("register_id", db.Integer, db.ForeignKey("register.id"))
    id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column("name", db.Unicode)
    sex = db.Column("sex", db.Unicode)
    cpf = db.Column("cpf", db.Integer)
    rg = db.Column("rg", db.Integer)
    crm = db.Column("crm", db.Integer)
    cel = db.Column("cel", db.Integer)
    phone = db.Column("phone", db.Integer)
    email = db.Column("email", db.Unicode)

    register = db.relationship("Register", foreign_keys=register_id)


class Institution(db.Model):
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
