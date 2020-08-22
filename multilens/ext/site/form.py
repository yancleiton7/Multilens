from wtforms import Form, PasswordField, StringField, validators


class FormLogin(Form):
    username = StringField("Usuario", [validators.Required()])
    passwd = PasswordField("Senha", [validators.Required()])
