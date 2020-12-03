$(window).load(function() {
    
    var quantidade_linhas = $("[name=load]").attr('id')


    for (i = -1; i < quantidade_linhas-1; i++) {
        
        if (i<0){
            $('#nome_fornecedor').attr({'name': "nome_fornecedorf", 'id':"nome_fornecedorf"})
            $('#valor').attr({'name': "valorf", 'id':"valorf"})
            $('#descricao').attr({'name': "descricaof", 'id':"descricaof"})
        }
        else{

        $('#nome_fornecedor').attr({'name': "nome_fornecedor"+i, 'id':"nome_fornecedor"+i})
        $('#valor').attr({'name': "valor"+i, 'id':"valor"+i})
        $('#descricao').attr({'name': "descricao"+i, 'id':"descricao"+i})
        }
      }
    
      $('#nome_fornecedorf').attr({'name': "nome_fornecedor", 'id':"nome_fornecedor"})
      $('#valorf').attr({'name': "valor", 'id':"valor"})
      $('#descricaof').attr({'name': "descricao", 'id':"descricao"})
    
    
});

$(document).ready(function() {
    
   
    
    (function ($) {
        $.fn.myfunction = function() {
    
        if (count_item<20){
            var div_complementar = $("#item-0").html()
            var div_adicinar = JSON.stringify(div_complementar)
            
            
            div_adicinar = JSON.parse(div_adicinar);

            div_adicinar = div_adicinar.replace('text" value="'+$("[name=nome_fornecedor]").val(), 'text" value="')
            div_adicinar = div_adicinar.replace('text" value="'+$("[name=valor]").val(), 'text" value="')
            div_adicinar = div_adicinar.replace('text" value="'+$("[name=descricao]").val(), 'text" value="')
            div_adicinar = div_adicinar.replace('name="nome_fornecedor', 'name="nome_fornecedor'+(count_item-1))
            div_adicinar = div_adicinar.replace('name="valor', 'name="valor'+(count_item-1))
            div_adicinar = div_adicinar.replace('name="descricao', 'name="descricao'+(count_item-1))

            div_adicinar = div_adicinar.replace('<div class="field is-grouped">', '<div class="field is-grouped" id="item-'+count_item+'">')
            

            $('#form_principal').append(div_adicinar); //add input box
    
               count_item+=1
               
               
        }
        };
        })( jQuery )

    var quantidade_linhas = $("[name=load]").attr('id')
    var count_item = parseInt(quantidade_linhas) 

    $("#novo_fornecedor").click(function () {
        
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