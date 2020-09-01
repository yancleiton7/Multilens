from flask import current_app
from flask_wtf import FlaskForm
from wtforms import (IntegerField, PasswordField, SelectField, StringField,
                     validators)
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.fields.html5 import EmailField
from wtforms.validators import Email, Length, Optional, Required

from multilens.ext.db.models import Institution, Speciality


class BaseForm(FlaskForm):
    def populate_obj(self, obj: FlaskForm):
        super(FlaskForm, self).populate_obj(obj)
        for field in self:
            if isinstance(field, QuerySelectField):
                setattr(obj, field.name, field.data.id)


class FormLogin(BaseForm):
    username = StringField("Usuario", [Required()])
    passwd = PasswordField("Senha", [Required()])


class FormDoctor(BaseForm):
    name = StringField("Nome", [Required("Informe o nome"), Length(min=5, max=50)])
    cpf = StringField("CPF", [Required("Informe o CPF"), Length(min=11, max=11)])
    rg = StringField("RG", [Required("Informe o RG"), Length(min=10, max=10)])
    crm = StringField("CRM", [Required("Informe o CRM"), Length(min=5, max=12)])
    cel = StringField(
        "Celular",
        [Required("Informe um número de celular valido"), Length(min=11, max=11)],
    )
    phone = StringField(
        "Telefone", [Required("Informe um telefone validio"), Length(min=10, max=10)]
    )
    email = EmailField("Email", [Required(), Email("Informe um e-mail valido")])
    speciality_id = QuerySelectField(
        "Especialidade",
        [Required("Selecione a especialidade")],
        get_label="speciality",
        get_pk=lambda x: x.id,
        query_factory=lambda: Speciality.query,
        allow_blank=True,
    )
    zip = StringField("CEP", [Required("Informe um CEP valido"), Length(min=8, max=8)])
    country = StringField("Cidade", [Required("Informe uma cidade")])
    address = StringField(
        "Endereço", [Required("Informe o endereço"), Length(min=1, max=70)]
    )
    district = StringField("Bairro", [Required("Informe o bairro"), ])


class FormInstitution(BaseForm):
    name = StringField("Nome", [Required("O nome da instituição é obrigatorio.")])
    cnpj = StringField("CNPJ", [Required("O CNPJ é obrigatório.")])
    adm_name = StringField("Administração")
    adm_email = EmailField("Adm. Email", [Optional(), Email("Informe um email valido")])
    adm_cel = StringField("Adm. Celular")
    adm_phone = StringField("Adm. Telefone")
    enf_name = StringField("Enfermagem")
    enf_email = EmailField("Enf. Email", [Optional(), Email("Informe um email valido")])
    enf_cel = StringField("Enf. Celular")
    enf_phone = StringField("Enf. Telefone")

    zip = StringField("CEP", [Required("Informe um CEP valido"), Length(min=8, max=8)])
    country = StringField("Cidade", [Required("Informe uma cidade")])
    address = StringField(
        "Endereço", [Required("Informe o endereço"), Length(min=1, max=70)]
    )
    district = StringField("Bairro", [Required("Informe o bairro"), ])
