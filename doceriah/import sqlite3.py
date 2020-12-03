import sqlite3
import random

conn = sqlite3.connect('doceriah.db')

cursor = conn.cursor()

# inserindo dados na tabela
for i in range(20000):
	tipo_item = ["Conta","Pedido"]
	conta = tipo_item[random.randrange(0, 2)]


	if conta=="Conta":
		tipo_forma = ["Anual","Mensal","Esporádico","Parcelado","Compras"]
		forma = tipo_forma[random.randrange(0, 5)]
	else:
		tipo_forma = ["Boleto","Transferência","Dinheiro"]
		forma = tipo_forma[random.randrange(0, 3)]

	
	data = str(random.randrange(10, 30))+"/"+str(random.randrange(1, 13))+"/"+str(random.randrange(2014, 2021))
	
	
	valor = str(random.randrange(100, 500))+","+str(random.randrange(10, 99))
	cursor.execute(f"""INSERT INTO financeiro (
	                           
	                           tipo_item,
	                           data_pagamento,
	                           descricao,
	                           id_item,
	                           tipo_forma,
	                           valor
	                       )
	                       VALUES (
	                          
	                           '{conta}',
	                           '2020-11-19',
	                           'Valores inseridos automaticamente',
	                           26,
	                           '{forma}',
	                           '{valor}'
	                       );
	""")

conn.commit()
conn.close()