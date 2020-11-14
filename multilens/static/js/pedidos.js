
$(document).ready(function() {
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
            $("#endereco_entrega").removeAttr('disabled');
            $("#endereco_entrega").val("")
        } else {
            $("#endereco_entrega").val("Retirar na loja.")
            $("#endereco_entrega").attr('disabled','disabled');
        }
        
    });

    $("#btn_salvar").click(function () {
        $("#endereco_entrega").removeAttr('disabled');

        });

    $("#novo_item").click(function () {

        if (count_item<20){
            var div_complementar = $("#repete").html()
            var div_adicinar = JSON.stringify(div_complementar)
            
            
            div_adicinar = JSON.parse(div_adicinar);
            div_adicinar = div_adicinar.replace('name="quantidade', 'name="quantidade'+count_item)
            div_adicinar = div_adicinar.replace('name="pedido', 'name="pedido'+count_item)
            div_adicinar = div_adicinar.replace('name="descricao', 'name="descricao'+count_item)
            div_adicinar = div_adicinar.replace('<div class="field is-grouped">', '<div class="field is-grouped" name="novo_item_'+count_item+'">')
            


            var pedido = "#pedidos-"+count_item;
            var wrapper = $(pedido); 
            $(wrapper).append(div_adicinar); //add input box

               count_item+=1

        }
    });



    $("#excluir_item").click(function () {
        if (count_item>0){
            count_item-=1
            var quantidade = "novo_item_"+count_item
            $("[name="+quantidade+"]").remove()
        }
        
    });


})


