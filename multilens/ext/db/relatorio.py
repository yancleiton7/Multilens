import io, xlwt, sqlite3
from .models import Cliente, Produto, Contas_parceladas, Balance, Pedidos, Financeiro, Contas, Pedido_item, Contas_pagas, Fornecedor
from . import db     

class Gerar_relatorios():

    def gerar_excel_aba_financeiro(workbook, inicio, fim):
        result = Financeiro.get_relatorio(inicio, fim)
        sheet = workbook.add_sheet('Financeiro')
        #add headers
        sheet.write(0, 0, 'Id')
        sheet.write(0, 1, 'Tipo de Item')
        sheet.write(0, 2, 'Data Pagamento')
        sheet.write(0, 3, 'Valor')
        sheet.write(0, 4, 'Descrição')
        sheet.write(0, 5, 'Tipo transação')

        idx = 0
        for financeiro in result:
            sheet.write(idx+1, 0, financeiro.id)
            sheet.write(idx+1, 1, financeiro.tipo_item)
            sheet.write(idx+1, 2, financeiro.get_data_pagamento())
            sheet.write(idx+1, 3, financeiro.valor)
            sheet.write(idx+1, 4, financeiro.descricao)
            sheet.write(idx+1, 5, financeiro.tipo_forma)
            idx += 1

        return workbook
    
    def gerar_excel_aba_contas(workbook, inicio, fim):
        result = Contas.get_relatorio(inicio, fim)
        sheet = workbook.add_sheet('Contas')
        #add headers
        sheet.write(0, 0, 'Id')
        sheet.write(0, 1, 'Descricao')
        sheet.write(0, 2, 'Fornecedor')
        sheet.write(0, 3, 'Valor')
        sheet.write(0, 4, 'Data Vencimento')
        sheet.write(0, 5, 'Observacao')
        sheet.write(0, 6, 'Status Pagamento')
        sheet.write(0, 7, 'Tipo Mensalidade')
        idx = 0
        for row in result:
            sheet.write(idx+1, 0, row.id)
            if row.tipo_mensalidade == "3":
                sheet.write(idx+1, 1, row.descricao+": "+str(len(row.parcelas_info))+"x de "+row.parcelas_info[0].valor)
            else:
                sheet.write(idx+1, 1, row.descricao)
            sheet.write(idx+1, 2, row.fornecedor)
            sheet.write(idx+1, 3, row.valor)
            sheet.write(idx+1, 4, row.get_data_vencimento())
            sheet.write(idx+1, 5, row.observacao)
            sheet.write(idx+1, 6, row.pagamento.status_pagamento_conta)
            sheet.write(idx+1, 7, row.recorrencia.tipo_mensalidade)
            idx += 1

        return workbook

    def gerar_excel_aba_contas_pagas(workbook, inicio, fim):

        result = db.session.query(Contas_pagas, Contas
        ).filter(Contas_pagas.data_pagamento>=inicio, Contas_pagas.data_pagamento<=fim
        ).join(Contas)
        
        sheet = workbook.add_sheet('Contas Pagas')
        #add headers
        sheet.write(0, 0, 'Id')
        sheet.write(0, 1, 'Descricao')
        sheet.write(0, 2, 'Fornecedor')
        sheet.write(0, 3, 'Data Vencimento')
        sheet.write(0, 4, 'Data Pagamento')
        sheet.write(0, 5, 'Valor')
        sheet.write(0, 6, 'Observacao')

        
        idx = 0
        for row in result:
            
            contas_pagas = row[0]
            contas = row[1]

            sheet.write(idx+1, 0, contas_pagas.id)
            if contas.tipo_mensalidade == "3":
                sheet.write(idx+1, 1, contas.descricao+" "+contas.get_formato_parcela() )
            else:
                sheet.write(idx+1, 1, contas.descricao)
            sheet.write(idx+1, 2, contas.fornecedor)
            sheet.write(idx+1, 3, contas_pagas.get_data_vencimento())
            sheet.write(idx+1, 4, contas_pagas.get_data_pagamento())
            sheet.write(idx+1, 5, contas_pagas.valor)
            sheet.write(idx+1, 6, contas_pagas.observacao)
            idx += 1

        return workbook

    def gerar_excel_aba_pedidos(workbook, inicio, fim):

        pedidos = Pedidos.get_relatorio(inicio, fim)
        
        sheet = workbook.add_sheet('Pedidos')
        
        #add headers
        sheet.write(0, 0, 'Id')
        sheet.write(0, 1, 'Data Pedido')
        sheet.write(0, 2, 'Id Cliente')
        sheet.write(0, 3, 'Nome Cliente')
        sheet.write(0, 4, 'Data Produção')
        sheet.write(0, 5, 'Hora Produção')
        sheet.write(0, 6, 'Data Entrega')
        sheet.write(0, 7, 'Hora Entrega')
        sheet.write(0, 8, 'Endereço de Entrega')
        sheet.write(0, 9, 'Tipo Retirada')
        sheet.write(0, 10, 'Status Entrega')
        sheet.write(0, 11, 'Data Pagamento')
        sheet.write(0, 12, 'Status Pagamento')
        sheet.write(0, 13, 'Tipo Pagamento')
        sheet.write(0, 14, 'Valor Total do Pedido')
        sheet.write(0, 15, 'Valor Entrega')
        sheet.write(0, 16, 'Valor Desconto')
        sheet.write(0, 17, 'Valor Final')
        sheet.write(0, 18, 'Observacao')


        idx = 0
        for pedido in pedidos:
            sheet.write(idx+1, 0, pedido.id)
            sheet.write(idx+1, 1, pedido.get_data_pedido())
            sheet.write(idx+1, 2, pedido.cliente.id)
            sheet.write(idx+1, 3, pedido.cliente.name)
            sheet.write(idx+1, 4, pedido.get_data_producao())
            sheet.write(idx+1, 5, pedido.hora_producao)
            sheet.write(idx+1, 6, pedido.get_data_entrega())
            sheet.write(idx+1, 7, pedido.hora_entrega)
            sheet.write(idx+1, 8, pedido.endereco_entrega)
            sheet.write(idx+1, 9, pedido.retirada.tipo_retirada)
            sheet.write(idx+1, 10, pedido.s_entrega.status_entrega)
            sheet.write(idx+1, 11, pedido.get_data_pagamento())
            sheet.write(idx+1, 12, pedido.s_pagamento.status_pagamento)
            sheet.write(idx+1, 13, pedido.pagamento.tipo_pagamento)
            sheet.write(idx+1, 14, pedido.valor)
            sheet.write(idx+1, 15, pedido.valor_entrega)
            sheet.write(idx+1, 16, pedido.valor_desconto)
            sheet.write(idx+1, 17, pedido.get_valor_final())
            sheet.write(idx+1, 18, pedido.observacao)
            idx += 1

        return workbook

    def gerar_excel_aba_item_pedidos(workbook, inicio, fim):

        pedidos = Pedidos.get_relatorio(inicio, fim)
        itens = []
        for pedido in pedidos:
            for item in pedido.pedidos_itens:
                itens.append(item) 


        sheet = workbook.add_sheet('Pedido Itens')
        
        #add headers
        sheet.write(0, 0, 'Id Pedido')
        sheet.write(0, 1, 'Id Cliente')
        sheet.write(0, 2, 'Nome do Cliente')
        sheet.write(0, 3, 'Data Cadastro')
        sheet.write(0, 4, 'Produto')
        sheet.write(0, 5, 'Descricao')
        sheet.write(0, 6, 'Quantidade')
        sheet.write(0, 7, 'Valor Unitário')
        sheet.write(0, 8, 'Valor Total')


        idx = 0
        for item in itens:
            sheet.write(idx+1, 0, item.pedido.id)
            sheet.write(idx+1, 1, item.pedido.cliente.id)
            sheet.write(idx+1, 2, item.pedido.cliente.name)
            sheet.write(idx+1, 3, item.pedido.get_data_pedido())
            sheet.write(idx+1, 4, item.pedido_nome.tipo)
            sheet.write(idx+1, 5, item.descricao)
            sheet.write(idx+1, 6, item.quantidade)
            sheet.write(idx+1, 7, item.valor_unitario)
            sheet.write(idx+1, 8, item.valor_total)
            idx += 1

        return workbook

    def gerar_excel_aba_produto(workbook, inicio, fim):
        result = Produto.get_relatorio(inicio, fim)
        sheet = workbook.add_sheet('Produtos')
        #add headers
        sheet.write(0, 0, 'Data Cadastro')
        sheet.write(0, 1, 'Id')
        sheet.write(0, 2, 'Grupo')
        sheet.write(0, 3, 'Nome do Produto')
        sheet.write(0, 4, 'Estoque Mínimo')
        sheet.write(0, 5, 'Unidade')
        sheet.write(0, 6, 'Observação')
        idx = 0
        for produto in result:
            sheet.write(idx+1, 0, produto.get_data_cadastro())
            sheet.write(idx+1, 1, produto.id)
            sheet.write(idx+1, 2, produto.grupo_nome.grupo)
            sheet.write(idx+1, 3, produto.nome_produto)
            sheet.write(idx+1, 4, produto.estoque_minimo)
            sheet.write(idx+1, 5, produto.unidade)
            sheet.write(idx+1, 6, produto.observacao)
            
            idx += 1

        return workbook

    def gerar_excel_aba_fornecedores(workbook, inicio, fim):

        produtos = Produto.get_relatorio(inicio, fim)
        forncedores = []
        for produto in produtos:
            for fornecedor in produto.fornecedor:
                forncedores.append(fornecedor) 

        
        sheet = workbook.add_sheet('Fornecedores')
        #add headers
        sheet.write(0, 0, 'Id Produto')
        sheet.write(0, 1, 'Nome do Produto')
        sheet.write(0, 2, 'Fornecedor')
        sheet.write(0, 3, 'Valor')
        sheet.write(0, 4, 'Descrição')

        idx = 0
        for fornecedor in forncedores:
            sheet.write(idx+1, 0, fornecedor.id_produto)
            sheet.write(idx+1, 1, fornecedor.produto.nome_produto)
            sheet.write(idx+1, 2, fornecedor.nome_fornecedor)
            sheet.write(idx+1, 3, fornecedor.valor)
            sheet.write(idx+1, 4, fornecedor.descricao)
            
            idx += 1

        return workbook

    def gerar_excel_aba_estoque(workbook, inicio, fim):
        result = Balance.get_relatorio(inicio, fim)
        sheet = workbook.add_sheet('Estoque')
        #add headers
        sheet.write(0, 0, 'Id Produto')
        sheet.write(0, 1, 'Nome do Produto')
        sheet.write(0, 2, 'quantidade')
        sheet.write(0, 3, 'Data')
        sheet.write(0, 4, 'Tipo')
        sheet.write(0, 5, 'Preço')
        sheet.write(0, 6, 'Observacao')

        idx = 0
        for produto_balance in result:
            sheet.write(idx+1, 0, produto_balance.item_id)
            sheet.write(idx+1, 1, produto_balance.product.nome_produto)
            sheet.write(idx+1, 2, produto_balance.quantidade)
            sheet.write(idx+1, 3, produto_balance.get_data())
            sheet.write(idx+1, 4, produto_balance.event)
            sheet.write(idx+1, 5, produto_balance.preco)
            sheet.write(idx+1, 6, produto_balance.observacao)
            
            idx += 1

        return workbook

    def gerar_excel_aba_clientes(workbook, inicio, fim):
        result = Cliente.get_relatorio(inicio, fim)
        sheet = workbook.add_sheet('Clientes')
        #add headers
        sheet.write(0, 0, 'Id Cliente')
        sheet.write(0, 1, 'Nome do Cliente')
        sheet.write(0, 2, 'Aniversario')
        sheet.write(0, 3, 'Data cadastro')
        sheet.write(0, 4, 'Endereço')
        sheet.write(0, 5, 'Observacao')

        idx = 0
        for cliente in result:
            sheet.write(idx+1, 0, cliente.id)
            sheet.write(idx+1, 1, cliente.name)
            sheet.write(idx+1, 2, cliente.get_aniversario())
            sheet.write(idx+1, 3, cliente.get_data_cadastro())
            sheet.write(idx+1, 4, cliente.register.get_endereco_s())
            sheet.write(idx+1, 5, cliente.observacao)
            
            idx += 1

        return workbook

    @staticmethod
    def gerar_excel(relatorio, inicio, fim):
        if inicio == "":
            inicio='1900-01-01'
        if fim=="":
            fim='2900-01-01'


        #output in bytes
        output = io.BytesIO()
        #create WorkBook object
        workbook = xlwt.Workbook()
        if relatorio=="tudo" or relatorio=="contas":
            
            workbook = Gerar_relatorios.gerar_excel_aba_contas(workbook, inicio, fim)
            workbook = Gerar_relatorios.gerar_excel_aba_contas_pagas(workbook, inicio, fim)

        if relatorio=="tudo" or relatorio=="estoque":
            workbook = Gerar_relatorios.gerar_excel_aba_produto(workbook, inicio, fim)
            workbook = Gerar_relatorios.gerar_excel_aba_fornecedores(workbook, inicio, fim)
            workbook = Gerar_relatorios.gerar_excel_aba_estoque(workbook, inicio, fim)

        if relatorio=="tudo" or relatorio=="pedido":    
            workbook = Gerar_relatorios.gerar_excel_aba_pedidos(workbook, inicio, fim)
            workbook = Gerar_relatorios.gerar_excel_aba_item_pedidos(workbook, inicio, fim)

        if relatorio=="tudo" or relatorio=="clientes": 
            workbook = Gerar_relatorios.gerar_excel_aba_clientes(workbook, inicio, fim)
        
        if relatorio=="tudo" or relatorio=="financeiro": 
            workbook = Gerar_relatorios.gerar_excel_aba_financeiro(workbook, inicio, fim)


        workbook.save(output)
        output.seek(0)
        return output
