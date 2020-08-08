from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from multilens.ext.db import db
from multilens.ext.db.models import Employees, Storage

admin = Admin()


class EmployeesModelView(ModelView):
    page_size = 10
    column_exclude_list = ['id', 'password']
    column_searchable_list = ['user', 'email', 'name']
    column_labels = {
        "user": "Usuario",
        "name": "Nome",
        "password": "Senha"
    }


class StorageModelView(ModelView):
    page_size = 10
    column_searchable_list = ['name', ]
    form_excluded_columns = ['avaliable', ]
    column_labels = {
        "name": "Produto",
        "price": "Preço",
        "unity": "Unidade"
    }

def init_app(app):
    admin.name = app.config.get("ADMIN_NAME", "Multilens")
    admin.index_view.is_visible = lambda: False
    admin.template_mode = app.config.get("ADMIN_TEMPLATE_MODE", "bootstrap3")
    admin.add_view(EmployeesModelView(Employees, db.session, "Funcionarios"))
    admin.add_view(StorageModelView(Storage, db.session, 'Produtos'))

    admin.init_app(app)
