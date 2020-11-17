$(document).ready(function() {

 
    
        $("#gerar_excel").click(function (e) {
            window.open('data:application/vnd.ms-excel,' + $('#tabela_2').html());
            e.preventDefault();
            alert("Em fase de desenvolvimento")
        });
})
