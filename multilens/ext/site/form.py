from flask import current_app
from wtforms import (Form, IntegerField, PasswordField, SelectField,
                     StringField, validators)
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.fields.html5 import EmailField
from wtforms.validators import Email, Length, Required

from multilens.ext.db.models import Institution


class FormLogin(Form):
    username = StringField("Usuario", [Required()])
    passwd = PasswordField("Senha", [Required()])


class FormDoctor(Form):
    name = StringField("Nome", [Required(), Length(min=5, max=50)])
    cpf = IntegerField("CPF", [Required(), Length(min=12, max=12)])
    rg = IntegerField("RG", [Required(), Length(min=11, max=11)])
    crm = IntegerField("CRM", [Required(), Length(min=5, max=12)])
    cel = IntegerField("Celular", [Required(), Length(min=12, max=12)])
    phone = IntegerField("Telefone", [Required(), Length(min=11, max=11)])
    email = EmailField("Email", [Required(), Email()])
    institution = QuerySelectField(
        "Instituição",
        [Required()],
        query_factory=lambda: [i.name for i in Institution.query.all()],
    )
    zip = IntegerField("CEP", [Required(), Length(min=8, max=8)])
    country = StringField("Cidade", [Required()])
    address = StringField("Endereço", [Required(), Length(min=1, max=70)])
    type = SelectField("Tipo", [Required()])
    speciality = SelectField("Especialidade", [Required()])
