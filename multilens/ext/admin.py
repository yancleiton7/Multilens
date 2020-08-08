from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from multilens.ext.db import db
from multilens.ext.db.models import Employees

admin = Admin()


class EmployeesModelView(ModelView):
    page_size = 10
    column_exclude_list = ['id', 'password']
    column_searchable_list = ['user', 'email', 'name']

def init_app(app):
    admin.name = app.config.get("ADMIN_NAME", "Multilens")
    admin.template_mode = app.config.get("ADMIN_TEMPLATE_MODE", "bootstrap3")
    admin.add_view(EmployeesModelView(Employees, db.session))

    admin.init_app(app)
