from flask import current_app, flash, redirect, request, url_for
from flask_admin import AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from wtforms import SelectField


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
            return redirect(url_for("login", next=request.url))

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
            return redirect(url_for("login", next=request.url))


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
            return redirect(url_for("login", next=request.url))


class UserModelView(BaseView):
    page_size = 10
    column_exclude_list = ["id", "password"]
    column_searchable_list = ["user", "email", "name"]
    column_labels = {"user": "Usuario", "name": "Nome", "password": "Senha"}


class GrupoModelView(BaseView):
    page_size = 10
    column_searchable_list = [
        "id", "grupo"
    ]
    column_labels = {"id": "id", "grupo": "Grupo"}

class PagamentoModelView(BaseView):
    page_size = 10
    column_searchable_list = [
        "tipo_pagamento"
    ]
    column_labels = {"id": "id", "tipo_pagamento": "Tipo de Pagamento"}

class StatusPagamentoContaModelView(BaseView):
    page_size = 10
    column_searchable_list = [
        "status_pagamento_conta"
    ]
    column_labels = {"id": "id", "status_pagamento_conta": "Status Contas"}

class TipoRetiradaContaModelView(BaseView):
    page_size = 10
    column_searchable_list = [
        "tipo_retirada"
    ]
    column_labels = {"id": "id", "tipo_retirada": "Tipo de Retirada"}

class StatusEntregaModelView(BaseView):
    page_size = 10
    column_searchable_list = [
        "status_entrega"
    ]
    column_labels = {"id": "id", "status_entrega": "Status Entrega"}

class StatusPagamentoModelView(BaseView):
    page_size = 10
    column_searchable_list = [
        "status_pagamento"
    ]
    column_labels = {"id": "id", "status_pagamento": "Status Pagamento"}

class TipoModelView(BaseView):
    page_size = 10
    column_searchable_list = [
        "tipo"
    ]
    column_labels = {"id": "id", "tipo": "Item do Pedido"}

class TipoMensalidadeModelView(BaseView):
    page_size = 10
    column_searchable_list = [
        "tipo_mensalidade"
    ]
    column_labels = {"id": "id", "tipo_mensalidade": "Mensalidade"}
