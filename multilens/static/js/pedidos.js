
$(document).ready(function() {

    (function ($) {
        $.fn.myfunction = function() {
               
        if (count_item<20){
            
            var div_complementar = $("#item").html()
            var div_adicinar = JSON.stringify(div_complementar)

            
            div_adicinar = JSON.parse(div_adicinar);
            div_adicinar = div_adicinar.replace('name="quantidade', 'name="quantidade'+count_item)
            div_adicinar = div_adicinar.replace('name="pedido', 'name="pedido'+count_item)
            div_adicinar = div_adicinar.replace('name="descricao', 'name="descricao'+count_item)
            div_adicinar = div_adicinar.replace('name="valor', 'name="valor'+count_item)
            div_adicinar = div_adicinar.replace('name="nome_fornecedor', 'name="nome_fornecedor'+count_item)
            div_adicinar = div_adicinar.replace('<div class="field is-grouped">', '<div class="field is-grouped" name="novo_item_'+count_item+'">')
            
    
            var pedido = "#item-"+count_item;
            var wrapper = $(pedido); 
            $(wrapper).append(div_adicinar); //add input box
    
               count_item+=1
               
        }
        };
        })( jQuery )

    var count_item = 0;
    
    $("#id_cliente").change(function () {
        var id_cliente = $(this).val()
        $.ajax({
            url: window.location.origin + "/api/clientes/" + id_cliente,
            type: "GET",
            success: function(response){
                
                $("#nome_cliente").val(response.name)
                $("#telefone").val(response.phone)
                $("#endereco").val(response.endereco)
            }
        })

    });

    $("#tipo_retirada").change(function () {
        var tipo_retirada =  $(this).find(":selected").text()
        if (tipo_retirada==="Delivery"){
            $("#endereco_entrega").attr('readonly', false);
            $("#endereco_entrega").val($("#endereco").val())
        } else {
            $("#endereco_entrega").val("Retirar na loja.")
            $("#endereco_entrega").attr('readonly', true);
        }
        
    });

    $("#btn_salvar").click(function () {
        $("#endereco_entrega").removeAttr('disabled');
        $("#id_cliente").removeAttr('disabled');
        $('#status_entrega option[value=1]').attr('selected','selected');
        });

    $("#salvar_conta").click(function () {
        
        tipo_mensalidade = $("#tipo_mensalidade").val()
        
        if (tipo_mensalidade==="3"){
            
        var valor_total = $('#valor').val().replace(",", ".")
        var valor_parcela = $('#valor_parcelas').val().replace(",", ".")
        var quantidade_parcelas = $('#parcelas').val()
        var total_calculado = (valor_parcela*quantidade_parcelas)

   
        if (total_calculado<valor_total && tipo_mensalidade==="3"){
            alert("O valor das parcelas x a quantidade de Parcelas é menor que o valor total.")
            
            $('#valor_parcelas').val("")
            }

        }
        });
         
    $("#novo_item").click(function () {
        
        $(this).myfunction()
    });

    $("#excluir_item").click(function () {
        if (count_item>0){
            count_item-=1
            var quantidade = "novo_item_"+count_item
            $("[name="+quantidade+"]").remove()
        }
        
    });

    $("#data_vencimento").change(function () {
            $("#data_pagamento").val($("#data_vencimento").val())

    });
  
    $("#tipo_mensalidade").change(function () {
        tipo_mensalidade = $(this).find(":selected").text()
        $("#parcelas").val(0)
        $("#valor_parcelas").val("00,00")
        $('#status_pagamento option[value=1 ]').attr('selected','selected');
        $("#Parcela").hide()
        $("#Valor_parcela").hide()
        $("#Status_pagamento").hide()
       
        
        
        if (tipo_mensalidade ==="Parcelado"){
            $("#Parcela").show()
            $("#Valor_parcela").show()

        } else if (tipo_mensalidade ==="Esporádico") {
            $("#Status_pagamento").show()
        } 
        
        

    });

    $("#parcelas").keyup(function () {
        var valor_total = $('#valor').val().replace(",", ".")
        var quantidade_parcelas = $('#parcelas').val()
        valor = valor_total/quantidade_parcelas
        
        if (quantidade_parcelas>1){
            valor_reais = valor.toString().split(".")[0]

            if (valor.toString().indexOf(".")>0){
                valor_centavos = valor.toString().split(".")[1].substr(0, 2)
            } else {
                valor_centavos = "00"
            }

            if (valor_centavos.length===1){valor_centavos = valor_centavos+"0"}
            if (valor_centavos.length===0){valor_centavos = "00"}
            if (valor_centavos.length===2){
                ultimo_digito_centavo = parseInt(valor_centavos.substr(1, 1))
                primeiro_digito_centavo = parseInt(valor_centavos.substr(0, 1))
                ultimo_digito_centavo = ultimo_digito_centavo +1
                if (ultimo_digito_centavo===10){
                    ultimo_digito_centavo = 0
                    primeiro_digito_centavo = primeiro_digito_centavo + 1
                    if (primeiro_digito_centavo===10){
                        primeiro_digito_centavo = 0
                        valor_reais = (parseInt(valor_reais)+1).toString()
                        }
                    }
                    valor_centavos = primeiro_digito_centavo.toString()+ultimo_digito_centavo.toString()
                }
            

            valor_final = valor_reais+","+valor_centavos
            
            $("#valor_parcelas").val(valor_final)
        }
        
        
    });


})


$(window).load(function() {

    
    var id_pedido = $("[name=id_form]").attr('id')
    var id_conta = id_pedido

    if (tipo_mensalidade==="Parcelado"){
        $("#Valor_parcela").show()
        $("#Parcela").show()

    }

    
    $.ajax({
        url: window.location.origin + "/api/contas/" + id_conta,
        type: "GET",
        success: function(response){
            $("#valor_parcelas").val("00,00")
            $("#parcelas").val(0)
            
            
            if (response.tipo_mensalidade==="3"){
                $("#Valor_parcela").show()
                $("#Parcela").show()
                $("#valor_parcelas").val(response.valor_parcelas)
                $("#parcelas").val(response.parcelas)
            }
            if (response.tipo_mensalidade==="4"){
                $("#Status_pagamento").show()
                $("#status_pagamento").val(response.status_pagamento)
            }
            $('#tipo_mensalidade option[value='+ response.tipo_mensalidade +']').attr('selected','selected');
            $('#status_pagamento option[value='+ response.status_pagamento +']').attr('selected','selected');
           
        }
    })

  
    var id_cliente = $("[name=load]").attr('id')
    
    $("#status_entrega_div").hide()
    
    $.ajax({
        url: window.location.origin + "/api/clientes/" + id_cliente,
        type: "GET",
        success: function(response){
            $("#nome_cliente").val(response.name)
            $("#telefone").val(response.phone)
            $("#endereco").val(response.endereco)
            $('#status_pagamento option[value='+ response.status_pagamento +']').attr('selected','selected');
            $("#id_cliente").val(id_cliente)
            $("#id_cliente").attr('readonly', true);
            $("#status_entrega_div").show()
           
        }
    })
    
    $.ajax({
        url: window.location.origin + "/api/pedido/" + id_pedido,
        type: "GET",
        success: function(response){
            $('#tipo_pagamento option[value='+ response.tipo_pagamento +']').attr('selected','selected');
            $('#status_pagamento option[value='+ response.status_pagamento +']').attr('selected','selected');
            $('#tipo_retirada option[value='+ response.tipo_retirada +']').attr('selected','selected');
            $('#status_entrega option[value='+ response.status_entrega +']').attr('selected','selected');
            //$("#endereco").val(response.endereco)
            
        }
    })
    
    //Depois de editar uma conta parcelada tem que aparecer o valor e as parcelas
    var tipo_mensalidade = $("#tipo_mensalidade").find(":selected").text()
    if (tipo_mensalidade==='Parcelado'){                
        $("#Valor_parcela").show()
        $("#Parcela").show()

    } else if (tipo_mensalidade==="Esporádico"){
        
            $("#Status_pagamento").show()
    }
    
});


