import datetime as dt
from datetime import datetime
from datetime import timedelta

from flask_login import UserMixin, current_user
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash
from sqlalchemy.sql import func

from . import db

db.metadata.clear()

def converter_data(data_a_converter):
    data_convertida = data_a_converter[-2:]+"/"+data_a_converter[5:7]+"/"+data_a_converter[:4]
    return data_convertida

def encriptar_telefone(telefone):
        telefone_encriptado = ""
        for indice, valor in enumerate(telefone):
            if indice<2 or indice>6:
                telefone_encriptado = telefone_encriptado+valor
            else:
                telefone_encriptado = telefone_encriptado+"*"
        return telefone_encriptado

def monthdelta(date, delta):
    m, y = (date.month+delta) % 12, date.year + ((date.month)+delta-1) // 12
    if not m: m = 12
    d = min(date.day, [31,
        29 if y%4==0 and not y%400==0 else 28,31,30,31,30,31,31,30,31,30,31][m-1])
    return date.replace(day=d,month=m, year=y)

def tratar_centavos(valor):
    valor_formatado =  str('{:.2f}').format(valor)
    valor_formatado = valor_formatado.replace(".", ",")
    return valor_formatado

class BaseModel:

    '''

    def populate_object(self, **data: dict) -> None:
        columns = self.__table__.columns.keys()
        for key, value in data.items():
            if key in columns:
                setattr(self, key, value)

    def to_dict(self) -> dict:
        return {col: getattr(self, col) for col in self.__table__.columns.keys()}

    def to_json(self) -> dict:
        data = self.to_dict()

        for col, value in data.items():
            if isinstance(value, dt.datetime) or isinstance(value, dt.date):
                data[col] = value.isoformat()

            elif isinstance(value, dt.time):
                data[col] = value.isoformat()[:8]

        return data

    def delete(self) -> None:
        db.session.delete(self)
        db.session.commit()

    def update(self, **data: dict) -> None:
        data = data.copy()

        for col in data.keys():
            if col not in self.editable_fields:
                data.pop(col, None)

        self.populate_object(**data)

        if "updated_at" in self.__table__.columns.keys():
            self.updated_at = dt.datetime.now()
            self.save()

    def save(self) -> dict:
        try:
            db.session.add(self)
            db.session.commit()

        except Exception as err:
            db.session.rollback()
            response = {
                "success": False,
                "message": f"Não foi possível salvar o {self.__name__}\nDescrição: {self.parse_exception(err)}",
            }

        else:
            response = {"success": True, "data": self.to_json()}

        return response

    def parse_exception(self, excp: Exception) -> str:
        return str(excp)
    '''


class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column("id", db.Integer, primary_key=True)
    user = db.Column("user", db.Unicode, unique=True)
    password = db.Column("password", db.Unicode)
    email = db.Column("email", db.Unicode)
    name = db.Column("name", db.Unicode)
    cpf = db.Column("cpf", db.Unicode)
    admin = db.Column("admin", db.Boolean)

    @staticmethod
    def create(user: str, password: str, email: str, cpf: str, admin=False):
        hash_passwd = generate_password_hash(password)
        user = User(user=user, password=hash_passwd, email=email, cpf=cpf, admin=admin)
        db.session.add(user)
        db.session.commit()

        return user

    @staticmethod
    def get(**kwargs):
        return User.query.filter_by(**kwargs).first()

    def update(self):
        pass

    @staticmethod
    def delete(**kwargs):
        User.query.filter_by(**kwargs).delete()
        db.session.commit()

    @property
    def is_admin(self):
        return self.admin

class Contas(db.Model):
    __tablename__ = "contas"
    id = db.Column("id", db.Integer, primary_key=True)
    descricao = db.Column("descricao", db.Unicode)
    fornecedor = db.Column("fornecedor", db.Unicode)
    data_vencimento = db.Column("data_vencimento", db.Unicode)
    valor = db.Column("valor", db.Unicode)
    status_pagamento = db.Column("status_pagamento", db.ForeignKey("pagamento_conta.id"))  
    observacao = db.Column("observacao", db.Unicode) 
    tipo_mensalidade = db.Column("tipo_mensalidade", db.ForeignKey("tipo_mensalidade.id"))  

    pagamento = db.relationship("Pagamento_conta", foreign_keys=status_pagamento)
    recorrencia = db.relationship("Tipo_mensalidade", foreign_keys=tipo_mensalidade)
    parcelas_info = db.relationship("Contas_parceladas", backref="owner")
    pagas_info = db.relationship("Contas_pagas", backref="owner")


    @staticmethod
    def get(id: int):
        return Contas.query.filter_by(id=id).first()

    @staticmethod
    def get_relatorio(inicio, fim):
        return Contas.query.filter(Contas.data_vencimento>=inicio, Contas.data_vencimento<=fim).all()

    @staticmethod
    def get_all():
        return Contas.query.order_by(Contas.id.desc()).all()

    def get_descricao(self):
        tipo_mensalidade = self.recorrencia.tipo_mensalidade
        quantidade = self.get_parcelas_pagas()
        if tipo_mensalidade == "Parcelado":
            return (f"Parcela: {quantidade-1} de {len(self.parcelas_info)} - {self.fornecedor} : {self.descricao}.")
        elif tipo_mensalidade == "Compras":
            return (f"Compras feitas em {self.fornecedor} ")
        else:
            return (f"{self.fornecedor} - Descrição: {self.descricao}")

    @staticmethod
    def get_pendentes():
        lista_de_contas = Contas.query.filter_by(status_pagamento=1).all()
        hoje = datetime.now().strftime('%Y%m')
        lista_pendentes_mes_atual = []
        for conta in lista_de_contas:
            vencimento = (conta.data_vencimento[:4]+conta.data_vencimento[5:7])
            if conta.recorrencia.tipo_mensalidade=="Anual":
                vencimento = (conta.data_vencimento[:4])
                ano = datetime.now().strftime('%Y')
                if vencimento <= ano:
                    lista_pendentes_mes_atual.append(conta)

            elif vencimento <= hoje:
                lista_pendentes_mes_atual.append(conta)

        return lista_pendentes_mes_atual

    @staticmethod
    def get_avencer_capa():
        hojeMais7 = datetime.now()+timedelta(days=7)
        return Contas.query.filter(Contas.status_pagamento==1, Contas.data_vencimento<hojeMais7
        ).order_by(Contas.data_vencimento.asc()).all()

    def get_data_vencimento(self):
        return converter_data(self.data_vencimento)

    def get_data_pagamento(self):
        return converter_data(self.data_pagamento)
    
    def get_parcelas_pagas(self):
        return Contas_parceladas.query.filter(Contas_parceladas.status_pagamento == 2, Contas_parceladas.id_conta == self.id).count()

    def get_parcela_atual(self):
        return self.get_parcelas_pagas()+1


    def get_formato_parcela(self):
        return str(self.get_parcela_atual())+"/"+str(len(self.parcelas_info))

    def get_parcelas_to_dict(self):
        response = {}
        for parcela in self.parcelas_info:
            if parcela is not None:
                response[parcela.id] = parcela.details
            else:
                response = {}

        return response

    def to_dict(self) -> dict:
        return dict((col, getattr(self, col)) for col in self.__table__.columns.keys())

    @property
    def details(self) -> dict:
        details = self.to_dict()
        #details.pop("register_id")
        return details


    def criar_parcelas(self, form):
        for i in range(int(form.parcelas.data)):
            item_parcela = Contas_parceladas()
            item_parcela.id_conta = self.id
            item_parcela.valor = form.valor_parcelas.data
            item_parcela.status_pagamento = 1

            data_vencimento = datetime.strptime(form.data_vencimento.data, '%Y-%m-%d').date()

            item_parcela.data_vencimento = monthdelta(data_vencimento, i)
            item_parcela.save()

    def deleta_parcelas(self):
        for parcela in self.parcelas_info:
            parcela.remove()
   
    @staticmethod
    def create_by_form(form):       
        conta = Contas()
        form.populate_obj(conta)
        response = conta.save()

        if conta.recorrencia.tipo_mensalidade=="Parcelado":
            conta.criar_parcelas(form)

        if conta.pagamento.status_pagamento_conta=="Pago":
            conta_paga = Contas_pagas()
            form.populate_obj(conta_paga)
            conta_paga.save()

        return response

    def update_by_form(self, form):
        form.populate_obj(self)
        response = self.save()

        if self.recorrencia.tipo_mensalidade=="Parcelado":
            self.deleta_parcelas()
            self.criar_parcelas(form)

        response["message"] = "Conta atualizada!"

        return response
    
    def save(self):
        try:
            db.session.add(self)
            db.session.commit()

        except:
            db.session.rollback()
            response = {
                "success": False,
                "message": "Aconteceu algo errado, por favor tente novamente",
            }

        else:
            response = {
                "success": True,
                "message": "Conta cadastrada com successo!",
                "id": self.id,
            }
       
        response["object"] = self
        return response

    def remove(self):
        if self.recorrencia.tipo_mensalidade=="Parcelado":
            self.deleta_parcelas()

        db.session.delete(self)
        db.session.commit()
        response = {"success": True, "message": "Produto excluido com sucesso!"}
        return response

class Contas_parceladas(db.Model):
    __tablename__ = "contas_parceladas"
    id = db.Column("id", db.Integer, primary_key=True)
    valor = db.Column("valor", db.Unicode)
    data_vencimento = db.Column("data_vencimento", db.Unicode)
    data_pagamento = db.Column("data_pagamento", db.Unicode, default="Pendente")
    status_pagamento = db.Column("status_pagamento", db.Integer, db.ForeignKey("pagamento_conta.id"))   
    id_conta = db.Column(db.Integer, db.ForeignKey("contas.id"))

    s_pagamento = db.relationship("Pagamento_conta", foreign_keys=status_pagamento)

    @staticmethod
    def get(id: int):
        return Contas_parceladas.query.filter_by(id=id).first()

    def to_dict(self) -> dict:
        return dict((col, getattr(self, col)) for col in self.__table__.columns.keys())

    @property
    def details(self) -> dict:
        details = self.to_dict()
        #details.pop("register_id")
        return details


    def save(self):
        try:
            db.session.add(self)
            db.session.commit()

        except:
            db.session.rollback()
            response = {
                "success": False,
                "message": "Aconteceu algo errado, por favor tente novamente",
            }

        else:
            response = {
                "success": True,
                "message": "Conta parcelada cadastrada com successo",
                "id": self.id,
            }
       
        response["object"] = self
        return response
    
    def remove(self):

        db.session.delete(self)
        db.session.commit()

class Contas_pagas(db.Model):
    __tablename__ = "contas_pagas"
    id = db.Column("id", db.Integer, primary_key=True)
    valor = db.Column("valor", db.Unicode)
    data_vencimento = db.Column("data_vencimento", db.Unicode)
    data_pagamento = db.Column("data_pagamento", db.Unicode)  
    id_conta = db.Column(db.Integer, db.ForeignKey("contas.id"))
    observacao = db.Column("observacao", db.Unicode) 

    @staticmethod
    def get(id: int):
        return Contas_pagas.query.filter_by(id=id).first()

    def get_data_pagamento(self):
        return converter_data(self.data_pagamento)
    
    def get_data_vencimento(self):
        return converter_data(self.data_vencimento)


    @staticmethod
    def create_by_form(form, conta_obj):

        conta_paga = Contas_pagas()
        form.populate_obj(conta_paga)
        conta_paga.id_conta = conta_obj.id


        if conta_obj.tipo_mensalidade == "1":
            data_vencimento = datetime.strptime(conta_obj.data_vencimento, '%Y-%m-%d').date()
            conta_obj.data_vencimento = monthdelta(data_vencimento, 1)


        elif conta_obj.tipo_mensalidade == "2":
            data_vencimento = datetime.strptime(conta_obj.data_vencimento, '%Y-%m-%d').date()
            conta_obj.data_vencimento = data_vencimento.replace(year=int(conta_obj.data_vencimento[:4])+1)
            
        
        elif conta_obj.tipo_mensalidade == "3":
            parcela_selecionada = ""
            proxima_parcela = "-"
            for parcela in conta_obj.parcelas_info:
                if parcela_selecionada!="":
                    proxima_parcela = parcela
                    break
                if parcela.data_pagamento == "Pendente":
                    parcela_selecionada = parcela


            parcela_selecionada.data_pagamento = conta_paga.data_pagamento
            parcela_selecionada.status_pagamento = 2
            parcela_selecionada.save()

            if proxima_parcela != "-":
                conta_obj.data_vencimento = proxima_parcela.data_vencimento
            else:
                conta_obj.status_pagamento = 2

                
            
        elif conta_obj.tipo_mensalidade == "4" or conta_obj.tipo_mensalidade == "5":
            conta_obj.status_pagamento = 2


        conta_obj.save()
        response = conta_paga.save()

        financeiro = Financeiro()
        financeiro.tipo_item = "Conta"
        financeiro.data_pagamento = conta_paga.data_pagamento
        financeiro.id_item = conta_paga.id
        financeiro.tipo_forma = conta_obj.recorrencia.tipo_mensalidade
        financeiro.descricao = conta_obj.get_descricao()
        financeiro.valor = conta_paga.valor
        
        financeiro.save()
        

        return response

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()

        except:
            db.session.rollback()
            response = {
                "success": False,
                "message": "Aconteceu algo errado, por favor tente novamente",
            }

        else:
            response = {
                "success": True,
                "message": "Conta parcelada cadastrada com successo",
                "id": self.id,
            }
       
        response["object"] = self
        return response
    
    def remove(self):

        db.session.delete(self)
        db.session.commit()

class Produto(db.Model):
    __tablename__ = "produtos"
    #balance = db.relationship("Balance", backref="balance", lazy="dynamic")


    id = db.Column("id", db.Integer, primary_key=True)
    nome_produto = db.Column("nome_produto", db.Unicode)
    grupo = db.Column("grupo", db.Integer, db.ForeignKey("grupo.id"))
    observacao = db.Column("observacao", db.Unicode)
    estoque_minimo = db.Column("estoque_minimo", db.Unicode)
    unidade = db.Column("unidade", db.Unicode)
    data_cadastro = db.Column("data_cadastro", db.Unicode, default=datetime.now().strftime('%Y-%m-%d'))
    fornecedor = db.relationship("Fornecedor", backref="owner")

    grupo_nome = db.relationship("Grupo", foreign_keys=grupo)

    @staticmethod
    def get_relatorio(inicio, fim):
        return Produto.query.filter(Produto.data_cadastro>=inicio, Produto.data_cadastro<=fim).all()



    @staticmethod
    def necessita_compra(id: int):
        minimo = Produto.get_minimo(id)
        estoque = Produto.get_balance(id)

        if estoque>minimo:
            return [False, "Prodtuo Disponível"]
        else:
            return [True, "Precisa comprar: "+str(minimo-estoque)]

    @staticmethod
    def necessita_compra_capa():
        return Produto.query.filter()

    @staticmethod
    def get_preco(id: int):
        balance = Balance.query.filter_by(item_id=id)
        preco = [i.preco for i in balance.filter_by(event="Entrada")]
        if len(preco)>1:
            preco = preco[-1:]
            preco = "R$ "+str(preco[0])
        elif len(preco)==1:
            preco = "R$ "+str(preco[0])
        else:
            preco = "Nenhuma entrada cadastrada"
        
        return preco

    @staticmethod
    def get_minimo(id: int):
        produto = Produto.query.filter_by(id=id).first()
        return produto.estoque_minimo
    
    @staticmethod
    def get_balance(id: int):

        balance = db.session.query(func.sum(Balance.quantidade
        ).label("Total")
        ).filter_by(item_id=id
        ).first()
        
        if balance[0] is None:
            resultado = 0
        else:
            resultado = balance[0]

        return resultado

    def get_data_cadastro(self):
        return converter_data(self.data_cadastro)

    @staticmethod
    def get_grupo(id: int):
        produto = Produto.query.filter_by(id=id).first()
        grupo = Grupo.get(produto.grupo).grupo
        return grupo

    @staticmethod
    def get_id(nome_produto: str):
        produto = Produto.query.filter_by(nome_produto=nome_produto).first()
        id = produto.id
        return id

    @staticmethod
    def get(id: int):
        return Produto.query.filter_by(id=id).first()

    @staticmethod
    def create_by_form(form):

        produto = Produto()
        form.populate_obj(produto)
        response = produto.save()

        return response

    def save(self):
        try:
           
            db.session.add(self)
            db.session.commit()

        except Exception as e:
            
            db.session.rollback()
            response = {
                "success": False,
                "message": "Aconteceu algo errado, verificar se produto já existe.",
            }

        else:
            response = {
                "success": True,
                "message": "Produto cadastrado com successo!",
                "object": self,
            }

        return response
    
    def update_by_form(self, form, lista_fornecedores):
        fornecedor = self.fornecedor
        
        form.populate_obj(self)
        response = self.save()
        
        
        form.populate_obj(fornecedor[0])
        fornecedor[0].id_produto = self.id
        fornecedor[0].save()

        for i in (range(int(len(lista_fornecedores)/3))):
            fornecedor.append(Fornecedor())
            form.populate_obj(fornecedor[i+1])
            fornecedor[i+1].id_produto = self.id
            fornecedor[i+1].valor = lista_fornecedores["valor"+str(i)]
            fornecedor[i+1].nome_fornecedor = lista_fornecedores["nome_fornecedor"+str(i)]
            fornecedor[i+1].descricao = lista_fornecedores["descricao"+str(i)]
            fornecedor[i+1].save()
        


        if not response["success"]:
            for i in (range(1+int(len(lista_fornecedores)/3))):
                fornecedor[i].remove()
        else:        
            response["message"] = "Produto editado com successo!"

        return response

    def update_fornecedores(self, lista_fornecedores):
        for fornecedor in self.fornecedor:
            fornecedor.remove()
        
        fornecedores = []
        fornecedores.append(Fornecedor())
        fornecedores[0].id_produto = self.id
        fornecedores[0].valor = lista_fornecedores["valor"]
        fornecedores[0].nome_fornecedor = lista_fornecedores["nome_fornecedor"]
        fornecedores[0].descricao = lista_fornecedores["descricao"]
        fornecedores[0].save()

        quantidade_repeticao = int(len(lista_fornecedores)/3)-1

        for i in range(quantidade_repeticao):
            fornecedores.append(Fornecedor())
            fornecedores[i+1].id_produto = self.id
            fornecedores[i+1].valor = lista_fornecedores["valor"+str(i)]
            fornecedores[i+1].nome_fornecedor = lista_fornecedores["nome_fornecedor"+str(i)]
            fornecedores[i+1].descricao = lista_fornecedores["descricao"+str(i)]
            fornecedores[i+1].save()
        

        

        response={}  
        response["success"] = "ok"
        response["message"] = "Fornecedores editados com successo!"
        return response
        
    def remove(self):
        db.session.delete(self)
        db.session.commit()
        response = {"success": True, "message": "Produto excluido com sucesso!"}

        return response

    def to_dict(self) -> dict:
        return dict((col, getattr(self, col)) for col in self.__table__.columns.keys())

    @staticmethod
    def get_all():
        return Produto.query.all()

class Fornecedor(db.Model):
    __tablename__ = "fornecedor"
    id = db.Column("id", db.Integer, primary_key=True)
    nome_fornecedor = db.Column("nome_fornecedor", db.Unicode)
    descricao = db.Column("descricao", db.Unicode)
    id_produto = db.Column(db.Integer, db.ForeignKey("produtos.id"))
    valor = db.Column("valor", db.Integer)

    produto = db.relationship("Produto", foreign_keys=id_produto)

    @staticmethod 
    def get_all():
        return Fornecedor.query.all()


    def remove(self):
        db.session.delete(self)
        db.session.commit()

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()

        except:
            db.session.rollback()
            response = {
                "success": False,
                "message": "Aconteceu algo errado, por favor tente novamente",
            }

        else:
            response = {
                "success": True,
                "message": "Fornecedor cadastrado com successo!",
                "id": self.id,
            }
       
        response["object"] = self
        return response

class Pedido_item(db.Model):
    __tablename__ = "pedidos_itens"
    id = db.Column("id", db.Integer, primary_key=True)
    produto = db.Column("produto", db.Unicode, db.ForeignKey("tipo.id"))
    descricao = db.Column("descricao", db.Unicode)
    id_pedido = db.Column(db.Integer, db.ForeignKey("pedidos.id"))
    quantidade = db.Column("quantidade", db.Integer)

    pedido_nome = db.relationship("Tipo", foreign_keys=produto)
    pedido = db.relationship("Pedidos", foreign_keys=id_pedido)

    @staticmethod
    def get_all():
        return Pedido_item.query.all()



    @staticmethod
    def get_itens(id_pedido):
        return Pedido_item.query.filter_by(id_pedido=id_pedido)

    def get(id: int):
        return Pedido_item.query.filter_by(id=id).first()
    
    def to_dict(self) -> dict:
        return dict((col, getattr(self, col)) for col in self.__table__.columns.keys())


    @property
    def details(self) -> dict:
        details = self.to_dict()
        return details

    def remove(self):
        db.session.delete(self)
        db.session.commit()

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()

        except:
            db.session.rollback()
            response = {
                "success": False,
                "message": "Aconteceu algo errado, por favor tente novamente",
            }

        else:
            response = {
                "success": True,
                "message": "Itens cadastrado com successo!",
                "id": self.id,
            }
       
        response["object"] = self
        return response

class Pedidos(db.Model):
    __tablename__ = "pedidos"
    id = db.Column("id", db.Integer, primary_key=True)
    data_pedido = db.Column("data_pedido", db.Unicode)
    data_entrega = db.Column("data_entrega", db.Unicode)
    data_pagamento = db.Column("data_pagamento", db.Unicode)
    hora_entrega = db.Column("hora_entrega", db.Unicode)
    id_cliente = db.Column(db.Integer, db.ForeignKey("cliente.id"))
    tipo_retirada = db.Column("tipo_retirada", db.Integer, db.ForeignKey("retirada.id"))
    tipo_pagamento = db.Column("tipo_pagamento", db.Integer, db.ForeignKey("pagamento.id"))
    endereco_entrega = db.Column("endereco_entrega", db.Unicode)
    status_pagamento = db.Column("status_pagamento", db.Integer, db.ForeignKey("status_pagamento.id"))   
    status_entrega = db.Column("status_entrega", db.Integer, db.ForeignKey("status_entrega.id") , default=1) 
    valor = db.Column("valor", db.Unicode)
    observacao = db.Column("observacao", db.Unicode)

    cliente = db.relationship("Cliente", foreign_keys=id_cliente)
    pagamento = db.relationship("Pagamento", foreign_keys=tipo_pagamento)
    pedidos_itens = db.relationship("Pedido_item", backref="owner")
    s_pagamento = db.relationship("Status_pagamento", foreign_keys=status_pagamento)
    s_entrega = db.relationship("Status_Entrega", foreign_keys=status_entrega)
    retirada = db.relationship("Retirada", foreign_keys=tipo_retirada)

    @staticmethod
    def get_relatorio(inicio, fim):
        return Pedidos.query.filter(Pedidos.data_pedido>=inicio, Pedidos.data_pedido<=fim).all()


    
    @staticmethod
    def get(id: int):
        return Pedidos.query.filter_by(id=id).first()

    def get_status_pagamento(self):
        return self.s_pagamento.status_pagamento

    def get_status_entrega(self):
        return self.s_entrega.status_entrega
        

    def get_data_entrega(self):        
        return converter_data(self.data_entrega)

    def get_data_pedido(self):
        return converter_data(self.data_pedido)

    def get_data_pagamento(self):
        return converter_data(self.data_pagamento)


    @staticmethod
    def get_all():
        result = Pedidos.query.order_by(Pedidos.data_entrega.asc(), Pedidos.hora_entrega.asc()).all()
        return result
     
    def get_pendentes_entrega():
        return Pedidos.query.order_by(Pedidos.data_entrega.asc(), Pedidos.hora_entrega.asc()).filter_by(status_entrega=1)

    def get_pendentes_pagamentos():
        return Pedidos.query.order_by(Pedidos.data_entrega.asc(), Pedidos.hora_entrega.asc()).filter(Pedidos.status_pagamento!=3)
 
    def get_pagos():
        return Pedidos.query.order_by(Pedidos.data_entrega.asc(), Pedidos.hora_entrega.asc()).filter(Pedidos.status_pagamento==3)

    @staticmethod
    def get_entrega_capa():
        hoje = datetime.today() + timedelta(days = 6)
        hoje = hoje.strftime('%Y-%m-%d')
        return Pedidos.query.filter(Pedidos.data_entrega<=hoje
        ).order_by(Pedidos.data_entrega.asc(), Pedidos.hora_entrega.asc()
        ).filter(Pedidos.status_entrega==1)

    def get_descricao_computada(self):
        descricao_computada = ""
        for pedidos_item in self.pedidos_itens:
            s = ""
            if pedidos_item.quantidade>0 and pedidos_item.pedido_nome.tipo!="Outros":
                s = "s"

            descricao_computada = descricao_computada + str(pedidos_item.quantidade) +": "+ pedidos_item.pedido_nome.tipo+s+" " + pedidos_item.descricao + "\n"
        
        return descricao_computada


    def to_dict(self) -> dict:
        return dict((col, getattr(self, col)) for col in self.__table__.columns.keys())

    @property
    def details(self) -> dict:
        details = self.to_dict()
        #details.pop("register_id")
        return details

    @staticmethod
    def create_by_form(form):
        pedido = Pedidos()
        form.populate_obj(pedido)
        response = pedido.save()
        return response


    def save(self):
        try:
            db.session.add(self)
            db.session.commit()

        except:
            db.session.rollback()
            response = {
                "success": False,
                "message": "Aconteceu algo errado, por favor tente novamente",
            }

        else:
            response = {
                "success": True,
                "message": "Pedido cadastrado com successo, cadastre agora os produtos!",
                "id": self.id,
                "object": self,
            }
       
        return response
    
    def update_by_form(self, form):
        form.populate_obj(self)
        response = self.save()
        response["message"] = "Pedido atualizado!"

        return response

    def update_pedidos(self, lista_pedido_itens):
                
        for pedido_item in self.pedidos_itens:
            pedido_item.remove()
        
        pedido_itens = []
        pedido_itens.append(Pedido_item())
        pedido_itens[0].id_pedido = self.id
        pedido_itens[0].quantidade = lista_pedido_itens["quantidade"]
        pedido_itens[0].produto = lista_pedido_itens["produto"]
        pedido_itens[0].descricao = lista_pedido_itens["descricao"]
        pedido_itens[0].save()

        quantidade_repeticao = int(len(lista_pedido_itens)/3)
        
        for i in range(1,quantidade_repeticao):
            
            pedido_itens.append(Pedido_item())
            pedido_itens[i].id_pedido = self.id
            pedido_itens[i].quantidade = lista_pedido_itens["quantidade"+str(i)]
            pedido_itens[i].produto = lista_pedido_itens["produto"+str(i)]
            pedido_itens[i].descricao = lista_pedido_itens["descricao"+str(i)]
            pedido_itens[i].save()
        
        response={}  
        response["success"] = "ok"
        response["message"] = "Produtos atualizado com successo!"
        return response
        

    def remove(self):
        for itens in self.pedidos_itens:
            itens.remove()

        db.session.delete(self)
        db.session.commit()
        response = {"success": True, "message": "Pedido excluido com sucesso!"}

        return response

class Balance(db.Model):
    __tablename__ = "balance"
    id = db.Column("id", db.Integer, primary_key=True)
    item_id = db.Column("item_id", db.Integer, db.ForeignKey("produtos.id"))
    quantidade = db.Column("quantidade", db.Integer)
    date = db.Column("date", db.Unicode)
    event = db.Column("event", db.Unicode)
    preco = db.Column("preco", db.Unicode, default="00,00")
    observacao = db.Column("observacao", db.Unicode)

    produto = db.relationship("Produto", foreign_keys=item_id)

    @staticmethod
    def get_relatorio(inicio, fim):
        return Balance.query.filter(Balance.date>=inicio, Balance.date<=fim).all()


    @staticmethod
    def get_balance_capa():
        
        balance = db.session.query(Produto.nome_produto, Produto.estoque_minimo,
        Produto.unidade, Produto.id,
            func.sum(Balance.quantidade).label("quantidade")
            ).group_by(Produto.id).join(Balance, isouter=True)

        return balance.all()
    
    def get_data(self):
        return converter_data(self.date)

    @staticmethod
    def get(id: int):
        return Balance.query.filter_by(id=id).first()

    @staticmethod
    def create_by_form(form):
        balance = Balance()
        form.populate_obj(balance)
        response = balance.save()
        return response

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()

        except Exception as e:
            db.session.rollback()
            response = {
                "success": False,
                "message": "Aconteceu algo errado, por favor tente novamente",
            }

        else:
            response = {
                "success": True,
                "message": "Alteração feita no estoque!",
                "object": self,
            }

        return response
    
    def update_by_form(self, form):
        form.populate_obj(self)
        response = self.save()
        response["message"] = "Produto editado com successo!"

        return response
    
    def remove(self):
        db.session.delete(self)
        db.session.commit()
        response = {"success": True, "message": "Produto excluido com sucesso!"}

        return response
    
    @staticmethod
    def get_all():
        return Balance.query.all()

class Tipo(db.Model):
    __tablename__ = "tipo"
    id = db.Column("id", db.Integer, primary_key=True)
    tipo = db.Column("tipo", db.Unicode)

    @staticmethod
    def get(id: int):
        return Tipo.query.filter_by(id=id).first()

class Grupo(db.Model):
    __tablename__ = "grupo"
    id = db.Column("id", db.Integer, primary_key=True)
    grupo = db.Column("grupo", db.Unicode)

    @staticmethod
    def get(id: int):
        return Grupo.query.filter_by(id=id).first()

class Retirada(db.Model):
    __tablename__ = "retirada"
    id = db.Column("id", db.Integer, primary_key=True)
    tipo_retirada = db.Column("tipo_retirada", db.Unicode)

    @staticmethod
    def get(id: int):
        return Retirada.query.filter_by(id=id).first()

class Tipo_mensalidade(db.Model):
    __tablename__ = "tipo_mensalidade"
    id = db.Column("id", db.Integer, primary_key=True)
    tipo_mensalidade = db.Column("tipo_mensalidade", db.Unicode)

    @staticmethod
    def get(id: int):
        return Tipo_mensalidade.query.filter_by(id=id).first()

class Pagamento(db.Model):
    __tablename__ = "pagamento"
    id = db.Column("id", db.Integer, primary_key=True)
    tipo_pagamento = db.Column("tipo_pagamento", db.Unicode)

    @staticmethod
    def get(id: int):
        return Pagamento.query.filter_by(id=id).first()

class Pagamento_conta(db.Model):
    __tablename__ = "pagamento_conta"
    id = db.Column("id", db.Integer, primary_key=True)
    status_pagamento_conta = db.Column("status_pagamento_conta", db.Unicode)

    @staticmethod
    def get(id: int):
        return Pagamento.query.filter_by(id=id).first()

class Status_pagamento(db.Model):
    __tablename__ = "status_pagamento"
    id = db.Column("id", db.Integer, primary_key=True)
    status_pagamento = db.Column("status_pagamento", db.Unicode)

    @staticmethod
    def get(id: int):
        return Status_pagamento.query.filter_by(id=id).first()

class Status_Entrega(db.Model):
    __tablename__ = "status_entrega"
    id = db.Column("id", db.Integer, primary_key=True)
    status_entrega = db.Column("status_entrega", db.Unicode)

    @staticmethod
    def get(id: int):
        return Status_Entrega.query.filter_by(id=id).first()

class Financeiro(db.Model):
    __tablename__ = "financeiro"
    id = db.Column("id", db.Integer, primary_key=True)
    id_item = db.Column("id_item", db.Integer)
    tipo_item = db.Column("tipo_item", db.Unicode)
    data_pagamento = db.Column("data_pagamento", db.Unicode)
    tipo_forma = db.Column("tipo_forma", db.Unicode)
    descricao = db.Column("descricao", db.Unicode)
    valor = db.Column("valor", db.Unicode)

    
    # .filter(Financeiro.data_pagamento>'2020-11-02')
    
    @staticmethod
    def get_relatorio(inicio, fim):
        return Financeiro.query.filter(Financeiro.data_pagamento>=inicio, Financeiro.data_pagamento<=fim).all()




    @staticmethod
    def get_all():
        return Financeiro.query.order_by(Financeiro.data_pagamento.desc()).all()

    def get_total_pedidos_valor(self):
        mes = datetime.now().strftime('%m')
        qry = db.session.query(func.sum(Financeiro.valor).label("total")).filter_by(tipo_item="Pedido")
        return tratar_centavos(qry.first()[0])

    def get_total_contas_valor(self):
        qry = db.session.query(func.sum(Financeiro.valor).label("total")).filter_by(tipo_item="Conta")
        return tratar_centavos(qry.first()[0])

    def get_total_pedidos(self):
        return Financeiro.query.filter_by(tipo_item="Pedido").count()

    def get_total_contas(self):
        return Financeiro.query.filter_by(tipo_item="Conta").count()

    def get_saldo(self):
        saida = float(self.get_total_contas_valor().replace(",","."))
        entrada = float(self.get_total_pedidos_valor().replace(",","."))
        return tratar_centavos(entrada-saida)

    def get_total_geral(self):
        qry = db.session.query(func.count(Financeiro.valor).label("total"))
        return qry.first()[0]
   
    @staticmethod
    def get_tipo(tipo):
        return Financeiro.query.filter_by(tipo_item=tipo).all()

    def get_data_registro(self):
        return converter_data(self.data_registro)

    def get_data_pagamento(self):
        return converter_data(self.data_pagamento)

    @staticmethod
    def get(id: int):
        return Financeiro.query.filter_by(id=id).first()

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()

        except:
            db.session.rollback()
            response = {
                "success": False,
                "message": "Aconteceu algo errado, por favor tente novamente",
            }

        else:
            response = {
                "success": True,
                "message": "Item Financeiro!",
                "id": self.id,
            }
       
        response["object"] = self
        return response

    def remove(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def create_by_form(form):
        financeiro = Financeiro()
        register = Register()

        form.populate_obj(register)
        register.type = "finaceiro"
        register.save()

        form.populate_obj(institution)
        financeiro.register_id = register.id

        response = financeiro.save()

        if not response["success"]:
            register.delete()

        return response

    def update_by_form(self, form):
        form.populate_obj(self)
        response = self.save()

        return response

    def to_dict(self):
        return dict((col, getattr(self, col)) for col in self.__table__.columns.keys())

class Register(db.Model):
    __tablename__ = "register"
    id = db.Column("id", db.Integer, primary_key=True)
    city = db.Column("city", db.Unicode)
    address = db.Column("address", db.Unicode)
    district = db.Column("district", db.Unicode)
    numero = db.Column("numero", db.Integer)
    estado = db.Column("estado", db.Unicode)
    complemento = db.Column("complemento", db.Unicode)

    type = db.Column("type", db.Unicode)

    @staticmethod
    def get(id):
        return Register.query.filter_by(id=id).first()

    @staticmethod
    def get_all():
        return Register.query.all()

    @staticmethod
    def get_endereco(id):
        register = Register.query.filter_by(id=id).first().to_dict()
        endereco = register["address"] + " - " + register["district"] + " - " + register["numero"] + " - " + register["complemento"]
        endereco = endereco + " - " + register["city"] +"/"+ register["estado"] 
        return endereco

    
    def get_endereco_s(self):
        register = self.to_dict()
        endereco = register["address"] + " - " + register["district"] + " - " + register["numero"] + " - " + register["complemento"]
        endereco = endereco + " - " + register["city"] +"/"+ register["estado"] 
        return endereco
            
    def save(self):
        try:
            db.session.add(self)
            db.session.commit()

        except:
            db.session.rollback()
            response = {
                "success": False,
                "message": "Aconteceu algo errado, por favor tente novamente",
            }

        else:
            response = {
                "success": True,
                "message": "Registro cadastrada com successo",
                "id": self.id,
            }
       
        response["object"] = self
        return response

    def to_dict(self):
        return dict((col, getattr(self, col)) for col in self.__table__.columns.keys())

    def remove(self):
        db.session.delete(self)
        db.session.commit()

    @property
    def details(self):
        address = self.to_dict()
        if self.type == "cliente":
            cliente = Cliente.query.filter_by(register_id=self.id).first()
            address.update({"cliente": cliente.details if cliente is not None else {}})

        elif self.type == "institution":
            institution = Financeiro.query.filter_by(register_id=self.id).first()
            address.update(
                {
                    "institution": institution.to_dict()
                    if institution is not None
                    else {}
                }
            )

        return address

    
    def __repr__(self):
        if self.type == "institution":
            return Financeiro.query.filter_by(register_id=self.id).first().name.capitalize()

        elif self.type == "cliente":
            return Register.query.filter_by(id=self.id).first()
            #return Register.query.filter_by(register_id=self.id).first().name.capitalize()
    
class Cliente(db.Model):
    __tablename__ = "cliente"
    id = db.Column("id", db.Integer, primary_key=True)
    register_id = db.Column("register_id", db.Integer, db.ForeignKey("register.id"))
    name = db.Column("name", db.Unicode)
    cel = db.Column("cel", db.Integer)
    email = db.Column("email", db.Unicode)
    aniversario = db.Column("aniversario", db.Unicode)
    observacao = db.Column("observacao", db.Unicode)
    data_cadastro = db.Column("data_cadastro", db.Unicode, default=datetime.now().strftime('%Y-%m-%d'))

    register = db.relationship("Register", foreign_keys=register_id)
    pedidos = db.relationship("Pedidos", backref="owner")

    @staticmethod
    def get_relatorio(inicio, fim):
        return Cliente.query.filter(Cliente.data_cadastro>=inicio, Cliente.data_cadastro<=fim).all()

    @staticmethod
    def create_by_form(form):
        cliente = Cliente()
        register = Register()

        form.populate_obj(register)
        register.type = "cliente"
        register.save()

        form.populate_obj(cliente)
        cliente.register_id = register.id

        response = cliente.save()

        if not response["success"]:
            register.delete()

        return response

    def update_by_form(self, form):
        form.populate_obj(self)
        form.populate_obj(self.register)
        self.register.save()
        response = self.save()

        return response

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()

        except IntegrityError:
            db.session.rollback()
            response = {
                "success": False,
                "message": "Já existe um cadastro com o mesmo CPF, RG ou CRM no banco de dados.",
            }

        else:
            response = {
                "success": True,
                "message": "Cliente cadastrado com successo!",
                "object": self,
            }

        return response

    def remove(self):
        
        for pedido in self.pedidos:
            pedido.remove()

        self.register.remove()
        db.session.delete(self)
        db.session.commit()
        response = {"success": True, "message": "Registro excluido com sucesso!"}

        return response

    @staticmethod
    def get_all():
        return Cliente.query.order_by(Cliente.id.desc()).all()

    @staticmethod
    def get(id: int):
        return Cliente.query.filter_by(id=id).first()

    @staticmethod
    def get_aniversariantes():
        mes_Atual = datetime.now().strftime('%m')
        Mes_procura = '%-{}-%'.format(mes_Atual)
        return Cliente.query.filter(Cliente.aniversario.like(Mes_procura)).all()

    def get_aniversario(self):
        return converter_data(self.aniversario)
    
    def get_telefone_encrypted(self):
        return encriptar_telefone(str(self.cel))

    def get_data_cadastro(self):
        return converter_data(self.data_cadastro)

    def get_data_aniversario(self):
        return converter_data(self.aniversario)

    def to_dict(self) -> dict:
        return dict((col, getattr(self, col)) for col in self.__table__.columns.keys())

    @property
    def details(self) -> dict:
        details = self.to_dict()
        details.pop("register_id")
        return details
