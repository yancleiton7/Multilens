from flask import flash, redirect, request, url_for
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user

from multilens.ext.db import db
from multilens.ext.db.models import Storage, User


class AdminView(AdminIndexView):
    @expose("/")
    def index(self):
        if not current_user.is_authenticated:
            flash("Essa página só está disponível para administradores.", "error")
            return redirect(url_for("site.login", next=request.url))

        if current_user.is_admin:
            return super().index()

        else:
            flash("Essa página só está disponível para administradores.", "error")
            return redirect(url_for("site.login", next=request.url))


class BaseView(ModelView):
    def is_accessible(self):
        if current_user.is_authenticated:
            return current_user.is_admin

        return False

    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            flash("Essa página só está disponível para administradores.", "error")
            return redirect(url_for("site.login", next=request.url))


class UserModelView(BaseView):
    page_size = 10
    column_exclude_list = ["id", "password"]
    column_searchable_list = ["user", "email", "name"]
    column_labels = {"user": "Usuario", "name": "Nome", "password": "Senha"}


class StorageModelView(BaseView):
    page_size = 10
    column_searchable_list = [
        "name",
    ]
    form_excluded_columns = [
        "avaliable",
    ]
    column_labels = {"name": "Produto", "price": "Preço", "unity": "Unidade"}


admin = Admin(index_view=AdminView())


def init_app(app):
    admin.name = app.config.get("ADMIN_NAME", "Multilens")
    admin.url = "/"
    admin.index_view.is_visible = lambda: False
    admin.template_mode = app.config.get("ADMIN_TEMPLATE_MODE", "bootstrap3")
    admin.add_view(UserModelView(User, db.session, "Funcionarios"))
    admin.add_view(StorageModelView(Storage, db.session, "Produtos"))

    admin.init_app(app)
