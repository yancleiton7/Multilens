import json
import os
import time

from flask import (Blueprint, current_app, flash, redirect, render_template,
                   request, send_file, url_for)
from flask_login import current_user, login_required

from multilens.ext.api.resources import ResourcePedido
from multilens.ext.db.models import Cliente, Estoque, Produto, Contas_parceladas, Balance, Pedidos, Financeiro, Contas, Pedido_item, Contas_pagas
                                        

from .form import (FormClientes, FormStatusPagamento, FormBalanceEntrada, FormPedido, FormFornecedor, FormParcelas,
                     FormBalanceSaida, FormProduto, FormContas, FormPedidoItens, FormStatusEntrega, FormContasPagas)

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


@bp.route("/financeiro/pedidos/", methods=["GET"])
@login_required
def financeiro_pedidos():
    return render_template("site/financeiro_pedidos.html", pedidos=Pedidos.get_pagos())

@bp.route("/contas/", methods=["GET"])
@login_required
def contas():
    return render_template("site/contas.html", contas=Contas.get_all())

@bp.route("/contas/pendentes", methods=["GET"])
@login_required
def contas_pendentes():
    return render_template("site/contas_pendentes.html", contas=Contas.get_pendentes())



@bp.route("/contas/cadastro", methods=["GET", "POST"])
@login_required
def form_contas():
    form = FormContas()
    if request.method == "GET":
        return render_template("forms/conta.html", form=form)

    elif request.method == "POST":
        if form.validate_on_submit():
            
            response = Contas.create_by_form(form)
            
            if response["success"]:
                flash(response["message"], "is-success")

            else:
                flash(response["message"], "is-danger")

        else:
            for field in form.errors.values():
                [flash(err, "is-danger") for err in field]

    return render_template("forms/conta.html", form=form)


@bp.route("/contas/<int:conta>", methods=["GET", "POST", "DELETE"])
@login_required
def financeiro(conta: int):
    form = FormContas()
    conta_selecionada = Contas.query.get_or_404(conta)

    if request.method == "GET":
        form.load(conta_selecionada)

    elif request.method == "POST":
        if form.validate_on_submit():
            
            response = conta_selecionada.update_by_form(form)
            
            if response["success"]:
                flash(response["message"], "is-success")

            else:
                flash(response["message"], "is-danger")

        else:
            
            for field in form.errors.values():
                [flash(err, "is-danger") for err in field]

    elif request.method == "DELETE":
        conta_selecionada = Contas.get(conta)

        if conta is not None:
            response = conta_selecionada.remove()

        else:
            response = {"success": False, "message": "Informe um registro valido"}

        return response

    return render_template("forms/conta.html", form=form)

@bp.route("/contas/pagamentos/<int:conta>", methods=["GET", "POST", "DELETE"])
@login_required
def status_pagamento_conta(conta: int):
    form = FormContasPagas()
    conta_obj = Contas.query.get_or_404(conta)
    conta_paga = Contas_pagas()
    

    if request.method == "GET":
        if conta_obj is None:
            flash("Cadastro não localizado!", "is-warning")
            redirect(url_for("site.financeiro"))
        else:
            form.load(conta_obj)
           

    elif request.method == "POST":
        print(request.form)
        if form.validate_on_submit():
            response = conta_paga.create_by_form(form, conta_obj)
            if response["success"]:
                flash(
                    response["message"],
                    "is-success",
                )
                return render_template("forms/contas_pagamentos.html", form=form)
                
            

            else:
                flash(response["message"], "is-danger")

        else:
            for field in form.errors.values():
                [flash(err, "is-danger") for err in field]

    return render_template("forms/contas_pagamentos.html", form=form)

@bp.route("/contas/parcelas/<int:conta_id>", methods=["GET", "POST"])
@login_required
def parcelas(conta_id: int):
    conta_obj = Contas.query.get_or_404(conta_id)
    if  len(conta_obj.parcelas_info)==0:
        conta_obj.parcelas_info.append(Contas_parceladas())

    form = FormParcelas()

    if request.method == "GET":
        if conta_obj is None:
            flash("Conta não localizada!", "is-warning")
            redirect(url_for("site.contas"))

        else: 
            form.load(conta_obj.parcelas_info[0])     

            
           

    elif request.method == "POST":
        print(request.form)
        if form.validate_on_submit():
            contagem_de_erro = 0
            for parcela in conta_obj.parcelas_info:
                try:
                    parcela.valor =request.form["valor"+str(parcela.id)]
                    parcela.status_pagamento =request.form["status_pagamento"+str(parcela.id)]
                    parcela.data_pagamento =request.form["data_pagamento"+str(parcela.id)]

                    if parcela.status_pagamento=="1":
                        parcela.data_pagamento ="Pendente"

                    
                    parcela.data_vencimento =request.form["data_vencimento"+str(parcela.id)]
                    parcela.save()
                except:
                    print(parcela.id)
                    contagem_de_erro += 1
                    parcela.valor =request.form["valor"]
                    parcela.status_pagamento =request.form["status_pagamento"]
                    parcela.data_pagamento =request.form["data_pagamento"]
                    parcela.data_vencimento =request.form["data_vencimento"]
                    parcela.save()

            

            if contagem_de_erro==1:
                flash(
                    "Parcelas atualizadas com sucesso.",
                    "is-success",
                )

                form.load(conta_obj.parcelas_info[0])

                return render_template("forms/parcelas.html", form=form, conta=conta_obj)
                
            

            else:
                
                flash("Algo aconteceu errado.", "is-danger")

        else:
            for field in form.errors.values():
                [flash(err, "is-danger") for err in field]


    return render_template("forms/parcelas.html", form=form, conta=conta_obj)


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
        return render_template("forms/produto.html", form=form, cadastro=True)

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

        return render_template("forms/produto.html", form=form, cadastro=True)

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
            lista_fornecedores = {}
             
            for i in range(21):
                  
                try:
                  lista_fornecedores["nome_fornecedor"+str(i)] =request.form["nome_fornecedor"+str(i)]
                  lista_fornecedores["valor"+str(i)] =request.form["valor"+str(i)]
                  lista_fornecedores["descricao"+str(i)] =request.form["descricao"+str(i)]
                except Exception as e:
                    print(e)
                    pass

                   
            response = produto.update_by_form(form, lista_fornecedores)

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

    return render_template("forms/produto.html", form=form, produto=produto)

@bp.route("/produto/fornecedor/<int:produto>", methods=["GET", "POST", "DELETE"])
@login_required
def fornecedores(produto: int):
    produto_selecionado = Produto.query.get_or_404(produto)
    form = FormFornecedor()
    form_fornecedores = []

    if request.method == "GET":
        if produto_selecionado is None:
            flash("Produto não localizado!", "is-warning")
            redirect(url_for("site.produto"))

        else:    
            for fornecedores in produto_selecionado.fornecedor: 
                form.load(fornecedores)
                form_fornecedores.append(form)
                form = FormFornecedor()
            
           

    elif request.method == "POST":
        if form.validate_on_submit():
           
            lista_fornecedores = {}
            lista_fornecedores["nome_fornecedor"] =request.form["nome_fornecedor"]
            lista_fornecedores["valor"] =request.form["valor"]
            lista_fornecedores["descricao"] =request.form["descricao"]
            for i in range(21):
                  
                try:
                  lista_fornecedores["nome_fornecedor"+str(i)] =request.form["nome_fornecedor"+str(i)]
                  lista_fornecedores["valor"+str(i)] =request.form["valor"+str(i)]
                  lista_fornecedores["descricao"+str(i)] =request.form["descricao"+str(i)]
                except:
                    pass
            
            
            response = produto_selecionado.update_fornecedores(lista_fornecedores)

            if response["success"]:
                flash(
                    response["message"],
                    "is-success",
                )
                for fornecedores in produto_selecionado.fornecedor: 
                    form.load(fornecedores)
                    form_fornecedores.append(form)
                    form = FormFornecedor()
                return render_template("forms/fornecedores.html", form=form_fornecedores, produto=produto_selecionado)
                
            

            else:
                
                flash(response["message"], "is-danger")

        else:
            for field in form.errors.values():
                [flash(err, "is-danger") for err in field]

    if len(form_fornecedores) ==0:
        form_fornecedores.append(form)
               

    return render_template("forms/fornecedores.html", form=form_fornecedores, produto=produto_selecionado)

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

@bp.route("/cozinha/", methods=["GET"])
@login_required
def cozinha():
    return render_template("site/cozinha.html", pedidos=Pedidos.get_pendentes_entrega())

@bp.route("/pagamentos/", methods=["GET"])
@login_required
def pagamentos():
    return render_template("site/pagamentos.html", pedidos=Pedidos.get_pendentes_pagamentos())

@bp.route("/entregas/", methods=["GET"])
@login_required
def entregas():
    return render_template("site/entregas.html", pedidos=Pedidos.get_pendentes_entrega())

@bp.route("/pedidos/", methods=["GET"])
@login_required
def pedidos():
    return render_template("site/pedidos.html", pedidos=Pedidos.get_all())

@bp.route("/pedido/novo", methods=["GET", "POST", "PUT", "DELETE"])
@login_required
def novo_pedido():
    form = FormPedido()
    if request.method == "GET":
        return render_template("forms/novo_pedido.html", form=form, cadastro=True)

    elif request.method == "POST":
        if form.validate_on_submit():

            response = Pedidos.create_by_form(form)

            if response["success"]:
                flash(
                    response["message"],
                    "is-success",
                )
                form.limpar()
                return redirect(url_for("site.itens_pedido", pedido_id=response["id"]))
                #return render_template("forms/novo_pedido.html", form=form, cadastro=True)
                
            

            else:
                flash(response["message"], "is-danger")

        else:
            for field in form.errors.values():
                [flash(err, "is-danger") for err in field]

        return render_template("forms/novo_pedido.html", form=form, cadastro=True)

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
            response = {"success": True, "message": "Pedido excuído com acesso."}

        else:
            
            response = {"success": False, "message": "Informe um registro valido"}

        return response

    return render_template("forms/novo_pedido.html", form=form)

@bp.route("/pedidos/itens/<int:pedido_id>", methods=["GET", "POST"])
@login_required
def itens_pedido(pedido_id: int):
    pedido_selecionado = Pedidos.query.get_or_404(pedido_id)
    if  len(pedido_selecionado.pedidos_itens)==0:
        pedido_selecionado.pedidos_itens.append(Pedido_item())

    form = FormPedidoItens()

    if request.method == "GET":
        if pedido_selecionado is None:
            flash("Pedido não localizado!", "is-warning")
            redirect(url_for("site.pedidos"))

        else: 
            form.load(pedido_selecionado.pedidos_itens[0])     

            
           

    elif request.method == "POST":
        if form.validate_on_submit():
            lista_pedidos_itens = {}
            lista_pedidos_itens["produto"] =request.form["produto"]
            lista_pedidos_itens["quantidade"] =request.form["quantidade"]
            lista_pedidos_itens["descricao"] =request.form["descricao"]

            for i in range(1,21):
                try:
                  
                  lista_pedidos_itens["produto"+str(i)] =request.form["produto"+str(i)]
                  lista_pedidos_itens["quantidade"+str(i)] =request.form["quantidade"+str(i)]
                  lista_pedidos_itens["descricao"+str(i)] =request.form["descricao"+str(i)]
                  
                except:
                    
                    break
                    
            
            
            response = pedido_selecionado.update_pedidos(lista_pedidos_itens)

            if response["success"]:
                flash(
                    response["message"],
                    "is-success",
                )

                form.load(pedido_selecionado.pedidos_itens[0])

                return render_template("forms/pedido_itens.html", form=form, pedido=pedido_selecionado)
                
            

            else:
                
                flash(response["message"], "is-danger")

        else:
            for field in form.errors.values():
                [flash(err, "is-danger") for err in field]


    return render_template("forms/pedido_itens.html", form=form, pedido=pedido_selecionado)

@bp.route("/pedidos/pagamentos/<int:pedido_id>", methods=["GET", "POST", "DELETE"])
@login_required
def status_pagamento_pedido(pedido_id: int):
    form = FormStatusPagamento()
    pedido_obj = Pedidos.query.get_or_404(pedido_id)
    
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
                flash(
                    response["message"],
                    "is-success",
                )
                return render_template("forms/pedidos_pagamentos.html", form=form)
                
            

            else:
                flash(response["message"], "is-danger")

        else:
            for field in form.errors.values():
                [flash(err, "is-danger") for err in field]

    return render_template("forms/pedidos_pagamentos.html", form=form)

@bp.route("/pedidos/entregas/<int:pedido_id>", methods=["GET", "POST", "DELETE"])
@login_required
def status_entrega_pedido(pedido_id: int):
    form = FormStatusEntrega()
    pedido_obj = Pedidos.query.get_or_404(pedido_id)
    
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
                flash(
                    response["message"],
                    "is-success",
                )
                return render_template("forms/pedidos_entregas.html", form=form)
                
            

            else:
                flash(response["message"], "is-danger")

        else:
            for field in form.errors.values():
                [flash(err, "is-danger") for err in field]

    return render_template("forms/pedidos_entregas.html", form=form)

