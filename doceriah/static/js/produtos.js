
$(document).ready(function() {
    
    $("#item_id").keyup(function () {
        var id = $(this).val()
        if (id===""){
            $("#nome_produto").val("")
        }
        else{
        $.ajax({
            url: window.location.origin + "/api/produtos/" + id,
            type: "GET",
            success: function(response){
                
                $("#nome_produto").val(response.nome_produto)
            }
        })
    }

    });

    $("#item_id").dblclick(function () {
        
        $("#article_produtos").show()
    });

    $("#item_id").focusout(function () {
        if ($("#item_id").val()!=""){
        $("#article_produtos").hide()
    }
    
    });

    $("#btn_salvar").click(function () {

        if ($("#nome_produto").val()===""){
            alert("Informe um Id válido.")
            $("#item_id").val("")
        }  
        });



})
