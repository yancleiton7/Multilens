$(document).ready(function () {
    $("div.buttons > strong > a.remove").bind("click", function () {

        var apagar = confirm('Deseja realmente excluir este registro?');
        var register = $(this).parent().parent().parent().parent()
        

        if (apagar){
            $.ajax({
                url: window.location.href + register.attr('id'),
                type: "DELETE",
                success: function () {
                    if ((window.location.href).includes('/fluxo/')){
                        var deletar = confirm('Você precisará alterar os status da Conta ou Pedido. Confirma exclusão?');
                        if(deletar){
                            register.remove()
                        }
                    }
                    else{
                        register.remove()
                    }
                   
                },
                error: function () {
                    alert(window.location.href + register.attr('id'))
                    alert("Não foi possível excluir o registro, tente novamente mais tarde.")
                }
            })
        }
    });
});

