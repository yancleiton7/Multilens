import json
import os
import time

from flask import (Blueprint, current_app, flash, redirect, render_template,
                   request, send_file, url_for)
from flask_login import current_user, login_required

from multilens.ext.api.resources import ResourceOrder
from multilens.ext.db.models import Cliente, Estoque, Produto, Balance, Pedidos

from .form import (FormClientes, FormFinishOrder, FormBalanceEntrada, FormPedido,
                     FormBalanceSaida, FormProduto, FormFinanceiro, FormOrderItems)

bp = Blueprint("site", __name__)


@bp.route("/", methods=["GET"])
def index():
    if not current_user.is_authenticated:
        return redirect(url_for("login"))

    return render_template("site/index.html")



@bp.route("/clientes/", methods=["GET", "DELETE"])
@login_required
def clientes():
    if request.method == "GET":
        if len(request.args)==0:
            return render_template("site/clientes.html", clientes=Cliente.get_all())
        else:
            return render_template("site/clientes.html", clientes=Cliente.get_aniversariantes(request.args))
    else:
        return render_template("site/clientes.html", clientes=Cliente.get_all())


@bp.route("/clientes/cadastro", methods=["GET", "POST"])
@login_required
def form_cliente():
    form = FormClientes()
    if request.method == "GET":
        return render_template("forms/cliente.html", form=form)

    elif request.method == "POST":
        if form.validate_on_submit():
            response = Cliente.create_by_form(form)

            if response["success"]:
                return redirect(url_for("site.clientes"))
                

            else:
                flash(response["message"], "is-danger")

        else:
            for field in form.errors.values():
                [flash(err, "is-danger") for err in field]

        return render_template("forms/cliente.html", form=form)


@bp.route("/clientes/<int:register>", methods=["GET", "POST", "DELETE"])
@login_required
def cliente(register: int):
    cliente_register = Cliente.query.get_or_404(register)
    form = FormClientes()

    if request.method == "GET":
        if cliente_register is None:
            flash("Cadastro não localizado!", "is-warning")
            redirect(url_for("site.form_cliente"))

        else:
            form.load(cliente_register)

    elif request.method == "POST":
        if form.validate_on_submit():
            response = cliente_register.update_by_form(form)

            if response["success"]:
                flash(response["message"], "is-success")

            else:
                flash(response["message"], "is-danger")

        else:
            for field in form.errors.values():
                [flash(err, "is-danger") for err in field]

    elif request.method == "DELETE":
        cliente_register = Cliente.get(register)

        if cliente_register is not None:
            response = cliente_register.remove()

        else:
            response = {"success": False, "message": "Informe um registro valido"}

        return response

    return render_template("forms/cliente.html", form=form)


@bp.route("/financeiro/", methods=["GET"])
@login_required
def financeiros():
    return render_template("site/financeiro.html", financeiros=Financeiro.get_all())


@bp.route("/financeiro/cadastro", methods=["GET", "POST"])
@login_required
def form_financeiro():
    form = FormFinanceiro()
    if request.method == "GET":
        return render_template("forms/financeiro.html", form=form)

    elif request.method == "POST":
        if form.validate_on_submit():
            response = Financeiro.create_by_form(form)

            if response["success"]:
                flash(response["message"], "is-success")

            else:
                flash(response["message"], "is-danger")

        else:
            for field in form.errors.values():
                [flash(err, "is-danger") for err in field]

    return render_template("forms/financeiro.html", form=form)


@bp.route("/financeiro/<int:register>", methods=["GET", "POST", "DELETE"])
@login_required
def financeiro(register: int):
    form = FormFinanceiro()
    financeiro_register = Financeiro.query.get_or_404(register)

    if request.method == "GET":
        form.load(financeiro_register)

    elif request.method == "POST":
        if form.validate_on_submit():
            response = financeiro_register.update_by_form(form)

            if response["success"]:
                flash(response["message"], "is-success")

            else:
                flash(response["message"], "is-danger")

        else:
            for field in form.errors.values():
                [flash(err, "is-danger") for err in field]

    elif request.method == "DELETE":
        financeiro_register = Financeiro.get(register)

        if financeiro is not None:
            response = financeiro_register.remove()

        else:
            response = {"success": False, "message": "Informe um registro valido"}

        return response

    return render_template("forms/financeiro.html", form=form)


@bp.route("/estoque", methods=["GET"])
@login_required
def estoques():
    return render_template(
        "site/estoque.html", products=Produto.query.all()
    )


@bp.route("/estoque/<int:produto>", methods=["GET", "POST", "DELETE"])
@login_required
def estoque(produto: int):
    
    form = FormProduto()
    produto = Produto.query.get_or_404(produto)

    if request.method == "GET":
        if produto is None:
            flash("Cadastro não localizado!", "is-warning")
            redirect(url_for("site.form_estoque"))

        else:
            form.load(produto)

    elif request.method == "POST":
        if form.validate_on_submit():
            response = produto.update_by_form(form)

            if response["success"]:
                flash(response["message"], "is-success")

            else:
                flash(response["message"], "is-danger")

        else:
            for field in form.errors.values():
                [flash(err, "is-danger") for err in field]

    elif request.method == "DELETE":
        produto = Produto.get(produto)

        if produto is not None:
            response = produto.remove()

        else:
            response = {"success": False, "message": "Informe um registro valido"}

        return response

    return render_template("forms/estoque.html", form=form)

@bp.route("/produtos/", methods=["GET", "DELETE"])
@login_required
def produtos():
        return render_template("site/produtos.html", produtos=Produto.get_all())

@bp.route("/produto/cadastro", methods=["GET", "POST"])
@login_required
def form_produto():
    form = FormProduto()
    if request.method == "GET":
        return render_template("forms/produto.html", form=form)

    elif request.method == "POST":
        if form.validate_on_submit():
            response = Produto.create_by_form(form)

            if response["success"]:
                flash(
                    response["message"],
                    "is-success",
                )
                form.limpar()
                return render_template("forms/produto.html", form=form)
                
            

            else:
                flash(response["message"], "is-danger")

        else:
            for field in form.errors.values():
                [flash(err, "is-danger") for err in field]

        return render_template("forms/produto.html", form=form)


@bp.route("/produtos/<int:register>", methods=["GET", "POST", "DELETE"])
@login_required
def produto(register: int):
    produto = Produto.query.get_or_404(register)
    form = FormProduto()

    if request.method == "GET":
        if produto is None:
            flash("Produto não localizado!", "is-warning")
            redirect(url_for("site.produto"))

        else:
            form.load(produto)

    elif request.method == "POST":
        if form.validate_on_submit():
            response = produto.update_by_form(form)

            if response["success"]:
                flash(response["message"], "is-success")

            else:
                flash(response["message"], "is-danger")

        else:
            for field in form.errors.values():
                [flash(err, "is-danger") for err in field]

    elif request.method == "DELETE":
        produto = Produto.get(register)

        if produto is not None:
            response = produto.remove()

        else:
            response = {"success": False, "message": "Informe um registro valido"}

        return response

    return render_template("forms/produto.html", form=form)


@bp.route("/balance/entrada", methods=["GET", "POST", "DELETE"])
@login_required
def form_produto_entrada():
    form = FormBalanceEntrada()
    if request.method == "GET":
        return render_template("forms/entrada.html", form=form)

    elif request.method == "POST":
        if form.validate_on_submit():
            form.event.data = "Entrada"
            form.item_id.data = Produto.get_id(form.produto.data.nome_produto)
            response = Balance.create_by_form(form)
            form.limpar()
            if response["success"]:
                flash(
                    response["message"],
                    "is-success",
                )
                return render_template("forms/entrada.html", form=form)
                
            

            else:
                flash(response["message"], "is-danger")

        else:
            for field in form.errors.values():
                [flash(err, "is-danger") for err in field]

        return render_template("forms/entrada.html", form=form)

@bp.route("/balance/saida", methods=["GET", "POST", "DELETE"])
@login_required
def form_produto_saida():
    form = FormBalanceSaida()
    if request.method == "GET":
        return render_template("forms/saida.html", form=form)

    elif request.method == "POST":
        if form.validate_on_submit():
            form.event.data = "Saida"
            form.item_id.data = Produto.get_id(form.produto.data.nome_produto)
            response = Balance.create_by_form(form)
            form.limpar()
            if response["success"]:
                flash(
                    response["message"],
                    "is-success",
                )
                return render_template("forms/saida.html", form=form)
                
            

            else:
                flash(response["message"], "is-danger")

        else:
            for field in form.errors.values():
                [flash(err, "is-danger") for err in field]

        return render_template("forms/saida.html", form=form)



@bp.route("/cozinha/", methods=["GET"])
@login_required
def cozinha():
    return render_template("site/cozinha.html", pedidos=Pedidos.get_pendentes_entrega())

@bp.route("/pagamentos/", methods=["GET"])
@login_required
def pagamentos():
    return render_template("site/pagamentos.html", pedidos=Pedidos.get_pendentes_pagamentos())

@bp.route("/pedidos/", methods=["GET"])
@login_required
def pedidos():
    return render_template("site/pedidos.html", pedidos=Pedidos.get_all())

'''
@bp.route("/vendas/", methods=["GET"])
@login_required
def sales():
    return render_template("site/cozinha.html", pedidos=Pedidos.get_pendentes())
'''


@bp.route("/vendas/nova", methods=["GET", "POST", "PUT", "DELETE"])
@login_required
def novo_pedido():
    form = FormPedido()
    if request.method == "GET":
        return render_template("forms/novo_pedido.html", form=form)

    elif request.method == "POST":
        if form.validate_on_submit():

            lista_pedidos = {}
            for i in range(21):
                try:
                  lista_pedidos["quantidade"+str(i)] =request.form["quantidade"+str(i)]
                  lista_pedidos["pedido"+str(i)] =request.form["pedido"+str(i)]
                  lista_pedidos["descricao"+str(i)] =request.form["descricao"+str(i)]
                except:
                    pass


            response = Pedidos.create_by_form(form, lista_pedidos)

            if response["success"]:
                flash(
                    response["message"],
                    "is-success",
                )
                form.limpar()
                return render_template("forms/novo_pedido.html", form=form)
                
            

            else:
                flash(response["message"], "is-danger")

        else:
            for field in form.errors.values():
                [flash(err, "is-danger") for err in field]

        return render_template("forms/novo_pedido.html", form=form)

@bp.route("/pedidos/<int:pedido>", methods=["GET", "POST", "DELETE"])
@login_required
def pedido(pedido: int):
    pedido_obj = Pedidos.query.get_or_404(pedido)
    form = FormPedido()
   
    if request.method == "GET":
        if pedido_obj is None:
            flash("Cadastro não localizado!", "is-warning")
            redirect(url_for("site.pedidos"))
            

        else:
            form.load(pedido_obj)

    elif request.method == "POST":
        if form.validate_on_submit():
            response = pedido_obj.update_by_form(form)

            if response["success"]:
                flash(response["message"], "is-success")

            else:
                flash(response["message"], "is-danger")

        else:
            for field in form.errors.values():
                [flash(err, "is-danger") for err in field]

    elif request.method == "DELETE":
        
        pedido_obj = Pedidos.get(pedido)

        if pedido_obj is not None:
            pedido_obj.remove()
            response = {"success": True, "message": "Informe um registro valido"}

        else:
            
            response = {"success": False, "message": "Informe um registro valido"}

        return response

    return render_template("forms/novo_pedido.html", form=form)



@bp.route("/vendas/<int:order_id>/checkout", methods=["GET", "POST"])
@login_required
def finish_sale(order_id: int):
    form = FormFinishOrder()
    order = Order.get(order_id)

    if order is None:
        flash(f"Não foi possível localizar a venda de Número {order_id}", "is-danger")

        return redirect(url_for("site.register_sale"))

    else:
        if order.is_finished:
            flash(
                f"A venda com o registro {order.id} já foi finalizada.",
                "is-warning",
            )
            return redirect(url_for("site.sales"))

        elif request.method == "GET":
            return render_template(
                "site/finish_order.html",
                form=form,
                order=order,
                order_details=order.get_details(),
            )

        elif request.method == "POST":
            if form.validate_on_submit():
                file_path = os.path.join(
                    current_app.root_path,
                    f"{current_app.config.get('ORDER_FOLDER', 'order')}/{order.id}.json",
                )
                form.populate_obj(order)
                order.finish()

                with open(file_path, "w", encoding="UTF-8") as f:
                    json.dump(
                        ResourceOrder().get(order.id), f, ensure_ascii=False, indent=4
                    )

                flash("Venda cadastrada com sucesso!", "is-success")
                return send_file(file_path, as_attachment=True)

            else:
                for field in form.errors.values():
                    [flash(err, "is-danger") for err in field]

        return render_template(
            "site/finish_order.html",
            form=form,
            order=order,
            order_details=order.get_details(),
        )
