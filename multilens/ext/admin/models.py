from flask import current_app, flash, redirect, request, url_for
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user


class AdminView(AdminIndexView):
    @expose("/")
    def index(self):
        if not current_user.is_authenticated:
            flash(
                current_app.config.get(
                    "MSG_ADMIN_ONLY",
                    "Essa página só está disponível para administradores.",
                ),
                "is-danger",
            )
            return redirect(url_for("site.login", next=request.url))

        if current_user.is_admin:
            return super().index()

        else:
            flash(
                current_app.config.get(
                    "MSG_ADMIN_ONLY",
                    "Essa página só está disponível para administradores.",
                ),
                "is-danger",
            )
            return redirect(url_for("site.login", next=request.url))


class BaseView(ModelView):
    def is_accessible(self):
        if current_user.is_authenticated:
            return current_user.is_admin

        return False

    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            flash(
                current_app.config.get(
                    "MSG_ADMIN_ONLY",
                    "Essa página só está disponível para administradores.",
                ),
                "is-danger",
            )
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


class SpecialityModelView(BaseView):
    column_editable_list = ["speciality"]
    column_labels = {"speciality": "Especialidade"}
