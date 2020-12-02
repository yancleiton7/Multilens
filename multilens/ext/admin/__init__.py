from flask_admin import Admin

from multilens.ext.db import db
from multilens.ext.db.models import (Balance, User, Grupo, Pagamento, Pagamento_conta, Retirada, Status_Entrega,
                                    Status_pagamento, Tipo, Tipo_mensalidade)


from .models import (AdminView, GrupoModelView, PagamentoModelView, StatusPagamentoContaModelView, TipoModelView,
                     UserModelView, TipoRetiradaContaModelView, StatusEntregaModelView, StatusPagamentoModelView,
                     TipoMensalidadeModelView)

admin = Admin(index_view=AdminView())


def init_app(app):
    admin.name = app.config.get("ADMIN_NAME", "Doceriah")
    admin.url = "/"
    admin.index_view.is_visible = lambda: False
    admin.template_mode = app.config.get("ADMIN_TEMPLATE_MODE", "bootstrap3")
    admin.add_view(UserModelView(User, db.session, "Funcionarios"))
    admin.add_view(TipoModelView(Tipo, db.session, "Item Pedido"))
    admin.add_view(GrupoModelView(Grupo, db.session, "Grupo"))
    admin.add_view(PagamentoModelView(Pagamento, db.session, "Tipo Pagamento"))
    admin.add_view(StatusPagamentoModelView(Status_pagamento, db.session, "Status Pagamento"))
    admin.add_view(StatusEntregaModelView(Status_Entrega, db.session, "Status Entrega"))
    admin.add_view(TipoRetiradaContaModelView(Retirada, db.session, "Tipo Retirada"))
    admin.add_view(TipoMensalidadeModelView(Tipo_mensalidade, db.session, "Mensalidade"))
    admin.add_view(StatusPagamentoContaModelView(Pagamento_conta, db.session, "Status Conta"))
    
    admin.init_app(app)
