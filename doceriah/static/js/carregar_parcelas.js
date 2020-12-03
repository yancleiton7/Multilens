

$(window).load(function() {

    
    var id_conta = $("[name=id_form]").attr('id')
    
    
    function retornar_conta(id) {
        var resposta
        
        $.ajax({
                
            url: window.location.origin + "/api/parcelas/" + id,
            type: "GET",
            async: false,
            success: function(response){
                
                resposta= response

            }
        });
        return resposta
      }
    
    
    var parcelas = retornar_conta(id_conta)
    var quantidade = 0
    
    $.each(parcelas, function(i, item) {
        if (quantidade===0){ quantidade=i}
        //$('#status_pagamento option[value='+ parcelas[i].status_pagamento +']').attr('selected','selected');
        $('#status_pagamento').attr({'name': 'status_pagamento'+i, 'id':"status_pagamento"+i})
        $('#valor').attr({'name': 'valor'+i, 'id':"valor"+i})
        $('#data_pagamento').attr({'name': 'data_pagamento'+i, 'id':"data_pagamento"+i})
        $('#data_vencimento').attr({'name': 'data_vencimento'+i, 'id':"data_vencimento"+i})
        $('#status_pagamento'+i+' option[value='+ parcelas[i].status_pagamento +']').attr('selected','selected');
       
        
    });

    
    $('#status_pagamento'+quantidade).attr({'name': 'status_pagamento', 'id':"status_pagamento"})
    $('#valor'+quantidade).attr({'name': 'valor', 'id':"valor"})
    $('#data_pagamento'+quantidade).attr({'name': 'data_pagamento', 'id':"data_pagamento"})
    $('#data_vencimento'+quantidade).attr({'name': 'data_vencimento', 'id':"data_vencimento"})  
    
    
});




