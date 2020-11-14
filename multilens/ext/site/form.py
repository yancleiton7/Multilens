from flask_wtf import FlaskForm
from wtforms import FloatField, PasswordField, StringField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.fields.html5 import EmailField
from wtforms.validators import Email, Length, Optional, Regexp, Required

from multilens.ext.db.models import ( Register, Estoque, Produto,Tipo, Retirada, Pagamento,
                                     Grupo,  Cliente, Status_pagamento)



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

    observacao = StringField("Observação", [Required("Caso não tenha observação preencher com -")])



    city = StringField("Cidade", [Required("Informe uma cidade")])
    estado = StringField("Estado", [Required("Informe um estado")])
    numero = StringField("Número", [Required("Necessário o número"), Regexp("^[0-9]*$", message="Informe somente números")])
    address = StringField("Endereço", [Required("Informe o endereço")])
    district = StringField("Bairro", [Required("Informe o bairro")])
    complemento = StringField("Complemento", [Required("Caso não haja complemento, colocar *.")])
    
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
        "Observação",
        [
            Required("Caso não tenha observação preencher com -"),
        ],
    )

    preco = StringField(
        "Preço",
        [
            Required("Preencher o preço utilizado"),
            Regexp("^[0-9]\d{0,4}(\.\d{3})*,\d{2}$", message="Informe somente números"),
        ],
    )

    date = StringField(
        "Data",
        [
            Regexp("\d{4}-\d{2}-\d{2}", message="Aniversário de ser no formato 01/01/2000"),
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
        "Observação",
        [
            Required("Caso não tenha observação preencher com -"),
        ],
    )


    date = StringField(
        "Data",
        [
            Regexp("\d{4}-\d{2}-\d{2}", message="Aniversário de ser no formato 01/01/2000"),
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
            Required("Preencher com o preço desse fornecedor"),
            Regexp("^[0-9]\d{0,4}(\.\d{3})*,\d{2}$", message="Informe somente números"),
        ],
    )

    descricao = StringField(
        "Informação adicional",
        [
           Required("Colocar informação adicional sobre esse fornecedor"),
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
        "Observação",
        [
            Required("Caso não tenha observação preencher com -"),
        ],
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

class FormFinanceiro(BaseForm):
    name = StringField("Nome", [Required("O nome da instituição é obrigatorio")])
    cnpj = StringField(
        "CNPJ",
        [
            Required("O CNPJ é obrigatório"),
            Regexp("^[0-9]*$", message="Informe somente números"),
        ],
    )
    adm_name = StringField("Administração")
    adm_email = EmailField("Adm. Email", [Optional(), Email("Informe um email valido")])
    adm_cel = StringField(
        "Adm. Celular",
        [
            Optional(),
            Regexp("^[0-9]*$", message="Informe somente números"),
            Length(
                min=11, max=11, message="O celular precisa conter exatamente 11 números"
            ),
        ],
    )
    adm_phone = StringField(
        "Adm. Telefone",
        [
            Optional(),
            Regexp("^[0-9]*$", message="Informe somente números"),
            Length(
                min=10,
                max=10,
                message="O telefone precisa conter exatamente 10 números",
            ),
        ],
    )
    enf_name = StringField("Enfermagem")
    enf_email = EmailField("Enf. Email", [Optional(), Email("Informe um email valido")])
    enf_cel = StringField(
        "Enf. Celular",
        [
            Optional(),
            Regexp("^[0-9]*$", message="Informe somente números"),
            Length(
                min=11, max=11, message="O celular precisa conter exatamente 11 números"
            ),
        ],
    )
    enf_phone = StringField(
        "Enf. Telefone",
        [
            Optional(),
            Regexp("^[0-9]*$", message="Informe somente números"),
            Length(
                min=10,
                max=10,
                message="O telefone precisa conter exatamente 10 números",
            ),
        ],
    )

    zip = StringField(
        "CEP",
        [
            Required("Informe um CEP valido"),
            Length(min=8, max=8, message="O CEP precisa conter exatamente 8 números"),
            Optional(),
            Regexp("^[0-9]*$", message="Informe somente números"),
        ],
    )
    city = StringField("Cidade", [Required("Informe uma cidade")])
    address = StringField(
        "Endereço",
        [
            Required("Informe o endereço"),
            Length(min=1, max=70, message="O endereço pode ter no máximo 70 caracters"),
        ],
    )
    district = StringField(
        "Bairro",
        [
            Required("Informe o bairro"),
        ],
    )

    def load(self, financeiro):
        self.process(obj=financeiro)

        if financeiro.register is not None:
            self.zip.data = financeiro.register.zip
            self.address.data = financeiro.register.address
            self.city.data = financeiro.register.city
            self.district.data = financeiro.register.district

class FormPedido(BaseForm):
    
    data_pedido = StringField(
        "Data pedido",
        [
            Regexp("\d{4}-\d{2}-\d{2}", message="Datas seguem o formato 01/01/2000"),
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

    valor_total = StringField(
        "Valor total do pedido",
        [
            Required("Preencher o preço utilizado"),
            Regexp("^[0-9]\d{0,4}(\.\d{3})*,\d{2}$", message="Informe somente números"),
        ],
    )

    #Depois que selecionar o cliente, aparecer telefone, aniversário e endereço.
    id_cliente = QuerySelectField(
        "Id do cliente",
        validators=[Required("O nome do cliente é obrigatorio!")],
        get_label="id",
        get_pk=lambda x: x.id,
        query_factory=lambda: Cliente.query,
        allow_blank=True,  
        
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

class FormOrder(BaseForm):
    freight = FloatField("Frete", validators=[Required("O frete é obrigatorio")])
    '''
    type_of_sale = QuerySelectField(
        "Tipo de venda",
        validators=[Required("O tipo de venda é obrigatorio!")],
        get_label="type_of_sale",
        get_pk=lambda x: x.id,
        query_factory=lambda: SaleType.query,
        allow_blank=True,
    )
    type_pgto = QuerySelectField(
        "Prazo Pgto.",
        validators=[Required("O prazo do pagamento é obrigatorio!")],
        get_label="type_of_payment",
        get_pk=lambda x: x.id,
        query_factory=lambda: PaymentType.query,
        allow_blank=True,
    )
    '''
    discount = FloatField("Desconto")

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
            Required("Por favor, preecher com observações, caso não tenha colocar '*."),
        ],
    )

    
    def load(self, pedido_itens):
        self.process(obj=pedido_itens)
        self.pedido_id = pedido_itens.id

class FormFinishOrder(BaseForm):
    register_id = QuerySelectField(
        "Cliente/Instituição",
        validators=[Required("Informe para quem será feita a venda")],
        get_pk=lambda x: x.id,
        query_factory=lambda: Register.query,
        allow_blank=True,
    )
