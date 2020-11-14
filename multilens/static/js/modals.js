$(document).ready(function () {
    $("div.buttons > strong > a.remove").bind("click", function () {

        var apagar = confirm('Deseja realmente excluir este registro?');
        var register = $(this).parent().parent().parent().parent()
        

        if (apagar){
            $.ajax({
                url: window.location.href + register.attr('id'),
                type: "DELETE",
                success: function () {
                    
                    register.remove()
                },
                error: function () {
                    alert("Não foi possível excluir o registro, tente novamente mais tarde.")
                }
            })
        }
    });
});

