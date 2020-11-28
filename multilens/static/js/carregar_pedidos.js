$(window).load(function() {

    var quantidade_linhas = $("[name=load]").attr('id')
    var id_pedido = $("[name=pedido_id]").attr('id')

    function retornar_pedido(id) {
        var resposta
        
        $.ajax({
                
            url: window.location.origin + "/api/pedido/" + id,
            type: "GET",
            async: false,
            success: function(response){
                
                resposta= response

            }
        });
        return resposta
      }
    


   
    var pedido = retornar_pedido(id_pedido)


    for (i = 0; i < quantidade_linhas; i++) {
        
        
        item_pedido = $("[name=id_pedido-"+i+"]").attr('id')
        
        $('#produto option[value='+ pedido[item_pedido] +']').attr('selected','selected'); 
        
        if (i===0){
            
            $('#produto').attr({'name': "profduto", 'id':"profduto"})
            $('#quantidade').attr({'name': "quanftidade", 'id':"quanftidade"})
            $('#descricao').attr({'name': "descrdicao", 'id':"descrdicao"})
            $('#valor_unitario').attr({'name': "valor_uncitario", 'id':"valor_uncitario"})
            $('#valor_total').attr({'name': "valor_totcal", 'id':"valor_totcal"})
        }
        else{
            
        $('#produto').attr({'name': "produto"+i, 'id':"produto"+i})
        $('#quantidade').attr({'name': "quantidade"+i, 'id':"quantidade"+i})
        $('#descricao').attr({'name': "descricao"+i, 'id':"descricao"+i})
        $('#valor_unitario').attr({'name': "valor_unitario"+i, 'id':"valor_unitario"+i})
        $('#valor_total').attr({'name': "valor_total"+i, 'id':"valor_total"+i})
        
        }
      }
      
      
      $('#profduto').attr({'name': "produto", 'id':"produto"})
      $('#quanftidade').attr({'name': "quantidade", 'id':"quantidade"})
      $('#descrdicao').attr({'name': "descricao", 'id':"descricao"})
      $('#valor_uncitario').attr({'name': "valor_unitario", 'id':"valor_unitario"})
      $('#valor_totcal').attr({'name': "valor_total", 'id':"valor_total"})
     
      

});

$(document).ready(function() {
    
    

     

    
    (function ($) {
        $.fn.gerar_multiplicacao = function() {
            if ($(this).attr('id')[0]==='v'){
                count_valor = $(this).attr('id').split('valor_unitario')[1]
            } else {
                count_valor = $(this).attr('id').split('quantidade')[1]
            }
            

            if ($('#valor_unitario'+count_valor).val()!='' && $('#quantidade'+count_valor).val()!=''){
                valor_unitario = parseFloat($('#valor_unitario'+count_valor).val().replace(",", "."))
                quantidade = parseInt($('#quantidade'+count_valor).val())
                valor_total = valor_unitario * quantidade
                reais = Math.trunc(valor_total)

                if(reais===valor_total){centavos="00"}
                else { 
                    centavos = valor_total.toString().split(",")[1]
                    if (centavos.length===1){centavos=centavos+"0"}
                }
                valor_input = reais.toString()+","+centavos
    
                $('#valor_total'+count_valor).val(valor_input)
            }

        }

        $.fn.myfunction = function() {
    
        if (count_item<20){
            var div_complementar = $("#item-0").html()
            var div_adicinar = JSON.stringify(div_complementar)
            
            
            div_adicinar = JSON.parse(div_adicinar);
            

            novo_nome_produto = '"produto'+count_item+'"'
            novo_nome_quantidade = '"quantidade'+count_item+'"'
            novo_nome_descricao = '"descricao'+count_item+'"'
            novo_nome_valor_unitario = '"valor_unitario'+count_item+'"'
            novo_nome_valor_total = '"valor_total'+count_item+'"'

            

            div_adicinar = div_adicinar.replace('name="produto"', "name="+novo_nome_produto)
            div_adicinar = div_adicinar.replace('name="quantidade"', "name="+novo_nome_quantidade)
            div_adicinar = div_adicinar.replace('name="descricao"', "name="+novo_nome_descricao)
            div_adicinar = div_adicinar.replace('name="valor_unitario"', "name="+novo_nome_valor_unitario)
            div_adicinar = div_adicinar.replace('name="valor_total"', "name="+novo_nome_valor_total)
            
            div_adicinar = div_adicinar.replace('id="produto"', "id="+novo_nome_produto)
            div_adicinar = div_adicinar.replace('id="quantidade"', "id="+novo_nome_quantidade)
            div_adicinar = div_adicinar.replace('id="descricao"', "id="+novo_nome_descricao)
            div_adicinar = div_adicinar.replace('id="valor_unitario"', "id="+novo_nome_valor_unitario)
            div_adicinar = div_adicinar.replace('id="valor_total"', "id="+novo_nome_valor_total)
            
            div_adicinar = div_adicinar.replace('text" value="'+$("[name=quantidade]").val(), 'text" value="')
            div_adicinar = div_adicinar.replace('text" value="'+$("[name=descricao]").val(), 'text" value="')
            div_adicinar = div_adicinar.replace('text" value="'+$("[name=valor_unitario]").val(), 'text" value="')
            div_adicinar = div_adicinar.replace('text" value="'+$("[name=valor_total]").val(), 'text" value="')
            div_adicinar = div_adicinar.replace('<div class="field is-grouped">', '<div class="field is-grouped" id="item-'+count_item+'">')
            console.log(div_adicinar)
            
              
            $('#form_principal').append(div_adicinar); //add input box

               count_item+=1
               
               
        }
        };
        })( jQuery )

    var quantidade_linhas = $("[name=load]").attr('id')
    var count_item = parseInt(quantidade_linhas) 


    $("#novo_produto").click(function () {
        
        $(this).myfunction()
    });

    $("#excluir_item").click(function () {
       
        if (count_item>1){
            
            count_item-=1
            var div_a_ser_excluida = "#item-"+count_item

            $(div_a_ser_excluida).remove()

        }
        
    });

    $('#form_principal').delegate('[id^=valor_unitario]','keyup', function (e) { 
        $(this).gerar_multiplicacao()

        tamanho = $(this).val().length
        if (tamanho===0){$(this).val("0,00")}
        tamanho = $(this).val().length
        $(this)[0].setSelectionRange(tamanho,tamanho)

        options = {
            prefix: '',
            suffix: '',
            fixed: true,
            fractionDigits: 2,
            decimalSeparator: ',',
            thousandsSeparator: '.',
            autoCompleteDecimal: true
          };
          

          SimpleMaskMoney.setMask(this, options)

    });

    $('#form_principal').delegate('[id^=quantidade]','keyup', function (e) { 
        $(this).gerar_multiplicacao()
    });
        
    $($('[id^=valor_unitario]')).keyup(function () {
        $(this).gerar_multiplicacao()

    });

    $($('[id^=quantidade]')).keyup(function () {
        $(this).gerar_multiplicacao()
    });

})