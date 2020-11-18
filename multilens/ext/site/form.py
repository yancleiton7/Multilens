from flask_wtf import FlaskForm
from wtforms import FloatField, PasswordField, StringField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.fields.html5 import EmailField
from wtforms.validators import Email, Length, Optional, Regexp, Required

from multilens.ext.db.models import ( Register, Estoque, Produto,Tipo, Retirada, Pagamento_conta, Pagamento,
                                     Grupo,  Cliente, Status_pagamento, Status_Entrega,Tipo_mensalidade, Contas)



class BaseForm(FlaskForm):
    def populate_obj(self, obj: FlaskForm):
        super(FlaskForm, self).populate_obj(obj)
        
        for field in self:
            if isinstance(field, QuerySelectField):
                setattr(obj, field.name, field.data.id)

class FormLogin(BaseForm):
    username = StringField("Usuario", [Required()])
    passwd = PasswordField("Senha", [Required()])

class FormClientes(BaseForm):
    name = StringField(
        "Nome",
        [
            Required("Informe o nome"),
            Length(min=5, max=50, message="O nome deve conter de 5 a 50 caracters"),
        ],
    )


    cel = StringField(
        "Celular",
        [
            Required("Informe um número de celular valido"),
            Length(
                min=11, max=11, message="O celular precisa conter exatamente 11 números 2 do DDD 9 do número"
            ),
            Regexp("^[0-9]*$", message="Informe somente números"),
        ],
    )
    phone = StringField(
        "Telefone",
        [
            Required("Informe um telefone validio"),
            Length(
                min=11,
                max=11,
                message="O telefone precisa conter exatamente 11 números 2 do DDD 9 do número ",
            ),
            Regexp("^[0-9]*$", message="Informe somente números"),
        ],
    )

    aniversario = StringField(
        "Nascimento",
        [
            Regexp("\d{4}-\d{2}-\d{2}", message="Data de nascimento deve ser no formato 01/01/2000"),
        ],
    )

    observacao = StringField("Observação")



    city = StringField("Cidade", [Required("Informe uma cidade")])
    estado = StringField("Estado", [Required("Informe um estado")])
    numero = StringField("Número", [Required("Necessário o número"), Regexp("^[0-9]*$", message="Informe somente números")])
    address = StringField("Endereço", [Required("Informe o endereço")])
    district = StringField("Bairro", [Required("Informe o bairro")])
    complemento = StringField("Complemento", )
    
    def load(self, cliente):
        self.process(obj=cliente)

        if cliente.register is not None:
            self.address.data = cliente.register.address
            self.city.data = cliente.register.city
            self.district.data = cliente.register.district
            self.numero.data = cliente.register.numero
            self.estado.data = cliente.register.estado
            self.complemento.data = cliente.register.complemento

class FormBalanceEntrada(BaseForm):
    produto = QuerySelectField(
        "Nome do Produto",
        validators=[Required("O produto é obrigatorio!")],
        get_label="nome_produto",
        get_pk=lambda x: x.id,
        query_factory=lambda: Produto.query,
        allow_blank=True,  
        
    )

    quantidade = StringField(
        "Quantidade",
        [        
            Regexp("^[0-9]*$", message="Informe somente números"),
        ],
    )

    observacao = StringField(
        "Observação"
    )

    preco = StringField(
        "Preço",
        [
            Required("Preencher com o preço do produto."),
            Regexp("^[0-9]\d{0,4}(\.\d{3})*,\d{2}$", message="Informe o valor no formato RR,cc ex: 45,22"),
        ],
    )

    date = StringField(
        "Data",
        [
            Regexp("\d{4}-\d{2}-\d{2}", message="Datas devem ser no formato 01/01/2000"),
        ],
    )

    event = StringField(
        "evento",
        [

        ]
    )

    item_id = StringField(
        "item_id",
        [

        ]
    )

    def limpar(self):
        self.date.data = ""
        self.quantidade.data = ""
        self.observacao.data = ""
        self.preco.data = ""
        self.produto.data = ""

class FormBalanceSaida(BaseForm):
    produto = QuerySelectField(
        "Nome do Produto",
        validators=[Required("O produto é obrigatorio!")],
        get_label="nome_produto",
        get_pk=lambda x: x.id,
        query_factory=lambda: Produto.query,
        allow_blank=True,  
        
    )

    quantidade = StringField(
        "Quantidade",
        [        
            Regexp("^[0-9]*$", message="Informe somente números"),
        ],
    )

    observacao = StringField(
        "Observação"
    )


    date = StringField(
        "Data",
        [
            Regexp("\d{4}-\d{2}-\d{2}", message="Datas devem ser no formato 01/01/2000"),
        ],
    )

    event = StringField(
        "evento",
        [

        ]
    )
    
    item_id = StringField(
        "item_id",
        [

        ]
    )

    def limpar(self):
        self.date.data = ""
        self.produto.data = ""
        self.quantidade.data = ""
        self.observacao.data = ""

class FormFornecedor(BaseForm):
    nome_fornecedor = StringField(
        "Fornecedor",
        [
            Required("Colocar o Fornecedor."),
        ],
    ) 

    valor = StringField(
        "Preço",
        [
            Required("Preencher com o preço nesse fornecedor"),
            Regexp("^[0-9]\d{0,4}(\.\d{3})*,\d{2}$", message="Informe o valor no formato RR,cc ex: 45,22"),
        ],
    )

    descricao = StringField(
        "Informação adicional",
        [
           
        ],
    )

    def load(self, fornecedor):
        self.process(obj=fornecedor)

class FormProduto(BaseForm):
    
    fornecedor = []
    nome_produto = StringField(
        "Nome do Produto",
        [
            Required("Informe o nome"),
        ],
    )


    grupo = QuerySelectField(
        "Grupo",
        validators=[Required("O grupo é obrigatorio!")],
        get_label="grupo",
        get_pk=lambda x: x.id,
        query_factory=lambda: Grupo.query,
        allow_blank=True,
        
        
    )


    unidade = StringField(
        "Unidade",
        [
            Required("Informe a unidade utilizada para esse produto."),
        ],
    )

    estoque_minimo = StringField(
        "Estoque mínimo",
        [
            
            Regexp("^[0-9]*$", message="Informe somente números"),
        ],
    )

    observacao = StringField(
        "Observação"
    )


    def load(self, produto):
        form_fornecedor = FormFornecedor()
        self.fornecedor = []

        for fornecedor in produto.fornecedor:
            form_fornecedor.load(fornecedor)
            self.fornecedor.append(form_fornecedor)

          
        self.process(obj=produto)
        
       

    def limpar(self):
        self.nome_produto.data = ""
        self.estoque_minimo.data = ""
        self.observacao.data = ""
        self.grupo.data = ""
        self.unidade.data = ""
        self.fornecedor = []

class FormContas(BaseForm):
    descricao_conta  = StringField("Descrição da Conta", [Required("Informar a descrição da conta")])
    fornecedor = StringField("Fornecedor", [Required("Registrar o fornecedor.")])
    valor  = StringField("Valor", [Required("Colocar o valor da conta"),
            Regexp("^[0-9]\d{0,4}(\.\d{5})*,\d{2}$", message="Informe o valor da conta no formato RR,cc ex: 45,22"),])
    
    status_pagamento = QuerySelectField(
        "Status do Pagamento",
        validators=[Required("O status do pagamento é obrigatoria!")],
        get_label="status_pagamento_conta",
        get_pk=lambda x: x.id,
        query_factory=lambda: Pagamento_conta.query,
        allow_blank=True,  
        
    )
    
    tipo_mensalidade = QuerySelectField(
        "Recorrencia",
        validators=[Required("Necessário selecionar tipo de mensalidade")],
        get_label="tipo_mensalidade",
        get_pk=lambda x: x.id,
        query_factory=lambda: Tipo_mensalidade.query,
        allow_blank=True,  
        
    )

    parcelas = StringField(
        "Parcelas",
        [       
            Required("Informar a quantidade de Parcelas."), 
            Regexp("^[0-9]*$", message="Informe somente números"),
        ],
    )

    valor_parcelas = StringField(
        "Valor das Parcelas",
        [        
            Required("Informar o valor das parcelas."),
            Regexp("^[0-9]\d{0,4}(\.\d{3})*,\d{2}$", message="Informe o valor das parcelas no formato RR,cc ex: 45,22"),
        ],
    )


    data_pagamento = StringField("Data Pagamento")
    data_vencimento  = StringField("Data Vencimento", [Required("Colocar a data de vencimento.")])
    observacao  = StringField("Observacao")

    def load(self, conta):
        self.process(obj=conta)
        self.id = conta.id

class FormPedido(BaseForm):
    
    data_pedido = StringField(
        "Data pedido",
        [
            Regexp("\d{4}-\d{2}-\d{2}", message="Data de pedido: Datas seguem o formato 01/01/2000"),
        ],
    )
    data_entrega = StringField(
        "Data entrega",
        [
            Regexp("\d{4}-\d{2}-\d{2}", message="Data de entrega: Datas seguem o formato 01/01/2000"),
        ],
    )
    hora_entrega = StringField(
        "Hora da Entrega",
        [
            Required("Por favor preencher hora da entrega."),
        ],
    )

    valor = StringField(
        "Valor total do pedido",
        [
            Required("Preencher com o valor do pedido, para contabilizar no Financeiro"),
            Regexp("^[0-9]\d{0,4}(\.\d{3})*,\d{2}$", message="Informe o valor no formato RR,cc ex: 45,22"),
        ],
    )

    observacao = StringField("Observações")

    id_cliente = StringField(
        "ID",
        [     
            Required("Preencher o Id do cliente"),   
            Regexp("^[0-9]*$", message="Informe somente números"),
        ],
    )

    tipo_retirada = QuerySelectField(
        "Forma de Retirada",
        validators=[Required("A forma de retirada é obrigatoria!")],
        get_label="tipo_retirada",
        get_pk=lambda x: x.id,
        query_factory=lambda: Retirada.query,
        allow_blank=True,  
        
    )
    
    #Caso o seja Delivery
    endereco_entrega = StringField(
        "Endereço Entrega",
        [        
            Required("Por favor, preecher o endereço."),
        ],
    )
    tipo_pagamento = QuerySelectField(
        "Forma de Pagamento",
        validators=[Required("A forma de Pagamento é obrigatoria!")],
        get_label="tipo_pagamento",
        get_pk=lambda x: x.id,
        query_factory=lambda: Pagamento.query,
        allow_blank=True,  
        
    )
    status_pagamento = QuerySelectField(
        "Status do Pagamento",
        validators=[Required("O status do pagamento é obrigatoria!")],
        get_label="status_pagamento",
        get_pk=lambda x: x.id,
        query_factory=lambda: Status_pagamento.query,
        allow_blank=True,  
        
    )
    status_entrega = QuerySelectField(
        "Status Entrega",
        get_label="status_entrega",
        get_pk=lambda x: x.id,
        query_factory=lambda: Status_Entrega.query,
        allow_blank=True,  
        
    )
    
    def load(self, pedido):
        self.process(obj=pedido)
        self.id = pedido.id



    def limpar(self):
        self.data_pedido.data = ""
        self.data_entrega.data = ""
        self.hora_entrega.data = ""
        self.endereco_entrega.data = ""
        self.id_cliente.data = ""
        self.tipo_retirada.data = ""
        self.tipo_pagamento.data = ""
        self.status_pagamento.data = ""

class FormPedidoItens(BaseForm):
    produto = QuerySelectField(
        "Produto",
        validators=[Required("O produto é obrigatorio!")],
        get_label="tipo",
        get_pk=lambda x: x.id,
        query_factory=lambda: Tipo.query,
        allow_blank=True
        
    )
    quantidade = StringField(
        "Quantidade",
        [        
            Regexp("^[0-9]*$", message="Informe somente números"),
        ],
    )
    descricao = StringField(
        "Descrição do Pedido",
        [        
            Required("Por favor, preecher com a descrição do pedido."),
        ],
    )

    
    def load(self, item_pedido):
        self.process(obj=item_pedido)
        self.pedido_id = item_pedido.id
        return ""

class FormStatusPagamento(BaseForm):
    status_pagamento = QuerySelectField(
        "Status do Pagamento",
        validators=[Required("O status do pagamento é obrigatoria!")],
        get_label="status_pagamento",
        get_pk=lambda x: x.id,
        query_factory=lambda: Status_pagamento.query,
        allow_blank=True,   
    )
    tipo_pagamento = QuerySelectField(
        "Forma de Pagamento",
        validators=[Required("A forma de Pagamento é obrigatoria!")],
        get_label="tipo_pagamento",
        get_pk=lambda x: x.id,
        query_factory=lambda: Pagamento.query,
        allow_blank=True,  
        
    )
    data_pagamento = StringField(
        "Data Pagamento",
        [
            Regexp("\d{4}-\d{2}-\d{2}", message="Datas seguem o formato 01/01/2000"),
        ],
    )
    observacao =  StringField("Observações")

    valor = StringField(
        "Valor total do pedido",
        [
            Required("Preencher com o valor do pedido, para contabilizar no Financeiro"),
            Regexp("^[0-9]\d{0,4}(\.\d{3})*,\d{2}$", message="Informe o valor no formato RR,cc ex: 45,22"),
        ],
    )

    


    def load(self, pedido):
        self.process(obj=pedido)
        self.id = pedido.id
        self.descricao = (f"Pedido :{pedido.id} - Cliente: {pedido.cliente.name} - Entrega: {pedido.get_data_entrega()}")

class FormStatusEntrega(BaseForm):
    tipo_retirada = QuerySelectField(
        "Forma de Retirada",
        validators=[Required("A forma de retirada é obrigatoria!")],
        get_label="tipo_retirada",
        get_pk=lambda x: x.id,
        query_factory=lambda: Retirada.query,
        allow_blank=True,  
        
    )

    status_entrega = QuerySelectField(
        "Status Entrega",
        validators=[Required("O Status de Entrega é obrigatório")],
        get_label="status_entrega",
        get_pk=lambda x: x.id,
        query_factory=lambda: Status_Entrega.query,
        allow_blank=True,  
        
    )

    
    
    endereco_entrega = StringField(
        "Endereço Entrega",
        [        
            Required("Por favor, preecher o endereço."),
        ],
    )
    data_entrega = StringField(
        "Data entrega",
        [
            Regexp("\d{4}-\d{2}-\d{2}", message="Datas seguem o formato 01/01/2000"),
        ],
    )

    hora_entrega = StringField(
        "Hora da Entrega",
        [
            Required("Por favor preencher hora da entrega."),
        ],
    )

    observacao =  StringField("Observações")


    


    def load(self, pedido):
        self.process(obj=pedido)
        self.id = pedido.id
        self.descricao = (f"Pedido :{pedido.id} - Cliente: {pedido.cliente.name} - Entrega: {pedido.get_data_entrega()}")

class FormContasPagas(BaseForm):

    data_pagamento = StringField(
        "Data Pagamento",
        [
            Regexp("\d{4}-\d{2}-\d{2}", message="Pagamento: Datas seguem o formato 01/01/2000"),
        ],
    )
    data_vencimento = StringField(
        "Data Vencimento",
        [
            Regexp("\d{4}-\d{2}-\d{2}", message="Vencimento: Datas seguem o formato 01/01/2000"),
        ],
    )

    valor = StringField(
        "Valor total do pagamento",
        [
            Required("Preencher com o valor pago nessa conta."),
            Regexp("^[0-9]\d{0,4}(\.\d{3})*,\d{2}$", message="Informe o valor no formato RR,cc ex: 45,22"),
        ],
    )

    observacao =  StringField("Observações")


    


    def load(self, conta_obj):
        
        self.descricao = (f"Conta :{conta_obj.id} - Fornecedor: {conta_obj.fornecedor} - Descrição: {conta_obj.descricao_conta}")
        self.process(obj=conta_obj)

        if conta_obj.tipo_mensalidade=="3":
            parcela_selecionada = ""
            for quantidade, parcela in enumerate(conta_obj.parcelas_info):
                if parcela.data_pagamento == "Pendente":
                    parcela_selecionada = parcela
                    self.descricao = (f"Parcela: {quantidade+1} de {len(conta_obj.parcelas_info)} - {conta_obj.fornecedor} : {conta_obj.descricao_conta}.")
                    self.process(obj=parcela_selecionada)
                    break


        self.id = conta_obj.id
        
class FormParcelas(BaseForm):

    data_pagamento = StringField(
        "Data Pagamento",
    )
    data_vencimento = StringField(
        "Data Vencimento",
        [
            Regexp("\d{4}-\d{2}-\d{2}", message="Vencimento: Datas seguem o formato 01/01/2000"),
        ],
    )

    status_pagamento = QuerySelectField(
        "Status do Pagamento",
        get_label="status_pagamento_conta",
        get_pk=lambda x: x.id,
        query_factory=lambda: Pagamento_conta.query,
        allow_blank=True,   
    )

    valor = StringField(
        "Valor da Parcela",
        [
            Required("Preencher com o valor da parcela."),
            Regexp("^[0-9]\d{0,4}(\.\d{3})*,\d{2}$", message="Parcela: Informe o valor no formato RR,cc ex: 45,22"),
        ],
    )

    observacao =  StringField("Observações")


    


    def load(self, parcela):
        self.process(obj=parcela)
        return ""
       
        
               
        
        