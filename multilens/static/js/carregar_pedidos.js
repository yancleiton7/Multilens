$(window).load(function() {

    var quantidade_linhas = $("[name=load]").attr('id')
    var id_pedido = $("[name=pedido_id]").attr('id')

    function retornar_clientes(id) {
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
    


   
    var pedido = retornar_clientes(id_pedido)


    for (i = 0; i < quantidade_linhas; i++) {
        
        
        item_pedido = $("[name=id_pedido-"+i+"]").attr('id')
        
        $('#produto option[value='+ pedido[item_pedido] +']').attr('selected','selected'); 
        
        if (i===0){
            
            $('#produto').attr({'name': "profduto", 'id':"profduto"})
            $('#quantidade').attr({'name': "quanftidade", 'id':"quanftidade"})
            $('#descricao').attr({'name': "descrdicao", 'id':"descrdicao"})
        }
        else{
            
        $('#produto').attr({'name': "produto"+i, 'id':"produto"+i})
        $('#quantidade').attr({'name': "quantidade"+i, 'id':"quantidade"+i})
        $('#descricao').attr({'name': "descricao"+i, 'id':"descricao"+i})
        
        }
      }
      
      
      $('#profduto').attr({'name': "produto", 'id':"produto"})
      $('#quanftidade').attr({'name': "quantidade", 'id':"quantidade"})
      $('#descrdicao').attr({'name': "descricao", 'id':"descricao"})
     
      

});

$(document).ready(function() {
    
   
    
    (function ($) {
        $.fn.myfunction = function() {
    
        if (count_item<20){
            var div_complementar = $("#item-0").html()
            var div_adicinar = JSON.stringify(div_complementar)
            
            
            div_adicinar = JSON.parse(div_adicinar);
            

            novo_nome_produto = 'name="produto'+count_item+'"'
            novo_nome_quantidade = 'name="quantidade'+count_item+'"'
            novo_nome_descricao = 'name="descricao'+count_item+'"'

            

            div_adicinar = div_adicinar.replace('name="produto"', novo_nome_produto)
            div_adicinar = div_adicinar.replace('name="quantidade"', novo_nome_quantidade)
            div_adicinar = div_adicinar.replace('name="descricao"', novo_nome_descricao)
            div_adicinar = div_adicinar.replace('text" value="'+$("[name=quantidade]").val(), 'text" value="')
            div_adicinar = div_adicinar.replace('text" value="'+$("[name=descricao]").val(), 'text" value="')
            div_adicinar = div_adicinar.replace('<div class="field is-grouped">', '<div class="field is-grouped" id="item-'+count_item+'">')
           
            
              
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
        
  


})