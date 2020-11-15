
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
        });

    $("#salvar_conta").click(function () {
        
  
        if (tipo_mensalidade===3){
        var valor_total = $('#valor').val().replace(",", ".")
        var valor_parcela = $('#valor_parcela').val().replace(",", ".")
        var quantidade_parcelas = $('#quantidade').val()
        var total_calculado = valor_parcela*quantidade_parcelas
        
        if (total_calculado<valor_total && tipo_mensalidade==="Parcelado"){
            alert("O valor das parcelas x a quantidade de Parcelas é menor que o valor total.")
            $('#valor_parcela').val("")
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
        $("#parcelas_pagas").val(0)
        $('#status_pagamento option[value=1 ]').attr('selected','selected');
        $("#Parcela").hide()
        $("#Parcela_paga").hide()
        $("#Valor_parcela").hide()
        $("#Status_pagamento").hide()
       
        

        if (tipo_mensalidade ==="Parcelado"){
            $("#Parcela").show()
            $("#Valor_parcela").show()
            $("#Parcela_paga").show()

        } else if (tipo_mensalidade ==="Esporádico") {
            $("#Status_pagamento").show()
        } 
        
        

});





        

})


$(window).load(function() {
    
    var id_pedido = $("[name=id_form]").attr('id')
    var id_conta = id_pedido

    
    $.ajax({
        url: window.location.origin + "/api/contas/" + id_conta,
        type: "GET",
        success: function(response){
            $("#valor_parcelas").val("00,00")
            $("#parcelas_pagas").val(0)
            $("#parcelas").val(0)
            
            
            if (response.tipo_mensalidade==="3"){
                
                $("#Valor_parcela").show()
                $("#Parcela_paga").show()
                $("#Parcela").show()
                $("#valor_parcelas").val(response.valor_parcelas)
                $("#parcelas_pagas").val(response.parcelas_pagas)
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
           
        }
    })
    
    $.ajax({
        url: window.location.origin + "/api/pedido/" + id_pedido,
        type: "GET",
        success: function(response){
            $('#tipo_pagamento option[value='+ response.tipo_pagamento +']').attr('selected','selected');
            $('#status_pagamento option[value='+ response.status_pagamento +']').attr('selected','selected');
            $('#tipo_retirada option[value='+ response.tipo_retirada +']').attr('selected','selected');
            $('#status_pagamento option[value='+ response.status_pagamento +']').attr('selected','selected');
            
        }
    })
    

    
});


