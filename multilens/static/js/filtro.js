$(document).ready(function() {

    var $rows = $('#tabela tbody tr');
    
    $('#filtro').keyup(function() {
        var val = $.trim($(this).val()).replace(/ +/g, ' ').toLowerCase();
        
        $rows.show().filter(function() {
            var text = $(this).text().replace(/\s+/g, ' ').toLowerCase();
            return !~text.indexOf(val);
        }).hide();


    });

    $('#filtro_Mes').change(function() {
        var val = $.trim($(this).val()).replace(/ +/g, ' ').toLowerCase();
        
        $rows.show().filter(function() {
            //var text = $(this).text().replace(/\s+/g, ' ').toLowerCase(); -- Essa linha procura em toda a correspondência
            var text = $(this).html().split('filtro_data')[1];

            return !~text.indexOf(val);
        }).hide();


    });


    $('#data_de').change(function() {
        var ate = $('#data_ate').val()
        var de = $('#data_de').val()
        if (ate!="" && de!=""){
           
            var ate_tratado = ate.split("-")
            var de_tratado = de.split("-")
            de_tratado = parseInt(de_tratado[0]+""+de_tratado[1]+""+de_tratado[2])
            ate_tratado = parseInt(ate_tratado[0]+""+ate_tratado[1]+""+ate_tratado[2])

            
            $rows.hide().filter(function() {
                var text = $(this).text().split("/")
                var entrega = parseInt(text[2].slice(0,4)+""+text[1].slice(-2)+""+text[0].slice(-2))
                return (entrega>=de_tratado && entrega<=ate_tratado)
            }).show();
            
        } else {
            $rows.show()
        }

    });

    $('#data_ate').change(function() {
        var ate = $('#data_ate').val()
        var de = $('#data_de').val()

        if (ate!="" && de!=""){
           
            var ate_tratado = ate.split("-")
            var de_tratado = de.split("-")
            de_tratado = parseInt(de_tratado[0]+""+de_tratado[1]+""+de_tratado[2])
            ate_tratado = parseInt(ate_tratado[0]+""+ate_tratado[1]+""+ate_tratado[2])

            
            $rows.hide().filter(function() {
                var text = $(this).text().split("/")
                var entrega = parseInt(text[2].slice(0,4)+""+text[1].slice(-2)+""+text[0].slice(-2))
                return (entrega>=de_tratado && entrega<=ate_tratado)
            }).show();
            
        } 

    });

    $("#imprimir").click(function () {
       

        $("#tabela").show()
        $("#desaparecer").hide()
        $("#desaparecer2").hide()
        $("#desaparecer3").hide()
        
        $("#id_footer").hide()
        window.print()
        $("#desaparecer").show()
        $("#desaparecer2").show()
        $("#desaparecer3").show()
        $("#id_footer").show()
        });

})
