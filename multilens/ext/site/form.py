from wtforms import Form, StringField, PasswordField, validators


class FormLogin(Form):
    username = StringField('Usuario', [validators.Required()])
    passwd = PasswordField('Senha', [validators.Required()])
