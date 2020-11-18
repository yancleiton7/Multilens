function tratar_data(data){
    var data_tratada = data.split("-")
    data_tratada = parseInt(data_tratada[0]+""+data_tratada[1]+""+data_tratada[2])
    
    return data_tratada
}

function procurar_fluxo($rows, val){
       
        var val = $.trim($("#filtro_Financeiro").val()).replace(/ +/g, ' ').toLowerCase() 
        var ate = $('#data_ate_financeiro').val()
        var de = $('#data_de_financeiro').val()
        var datas_vazias = true
        if (ate!="" && de!=""){
            ate = tratar_data(ate)
            de = tratar_data(de)
            datas_vazias = false
        }
    
    var valor_entrada=0
    var count_entrada = 0
    var valor_saida=0
    var count_saida =0
    var saldo = 0
    var transacoes = 0
    var tipo = '[entrada]'

        

    

    $rows.hide().filter(function() {
        valor_em_html= $(this).html().split('R$ ')[1].split('  </td>')[0];
        var text = $(this).text().replace(/\s+/g, ' ').toLowerCase()
        var data = $(this).text().split("/")
        var data_tratada = parseInt(data[2].slice(0,4)+""+data[1].slice(-2)+""+data[0].slice(-2))



        console.log("Datas")
        console.log((data_tratada>=de && data_tratada<=ate))
           // console.log(((text.indexOf(val)>0 || val==="") && ((ate!="" && de!="")&&(data_tratada>=val[0] && data_tratada<=val[1]))))
            
            if ((text.indexOf(val)>0 || val==="") && (datas_vazias || (data_tratada>=de && data_tratada<=ate))){
                
                if (text.indexOf(tipo)>0){   
                    count_entrada +=1     
                    valor_entrada = valor_entrada + parseFloat(valor_em_html.replace(",","."))
                } else {
                    count_saida +=1  
                    valor_saida = valor_saida + parseFloat(valor_em_html.replace(",","."))
                }
                
                
            } 
            
            return ((text.indexOf(val)>0 || val==="") && (datas_vazias || (data_tratada>=de && data_tratada<=ate)));
            
        

    }).show();

    saldo = (valor_entrada-valor_saida).toFixed(2).toString().replace(".",",")
    transacoes = (count_entrada+count_saida)
    valor_entrada = valor_entrada.toFixed(2).toString().replace(".",",")
    valor_saida = valor_saida.toFixed(2).toString().replace(".",",")
    
    //valor_entrada = valor_entrada.toSring().split(".")[0]+","+valor_entrada.toSring().split(".")[1].substr(0, 2)
    $('#Entrada').text(valor_entrada)
    $('#Saida').text(valor_saida)
    $('#Saldo').text(saldo)
    $('#Entrada_contador').text(count_entrada)
    $('#Saida_contador').text(count_saida)
    $('#Saldo_contador').text(transacoes)
}


function filtro_normal($rows, val, caller="caller"){

        $rows.show().filter(function() {
            if (caller==="caller") {var text = $(this).text().replace(/\s+/g, ' ').toLowerCase();}
            if (caller==="Filtro_mes") {var text = $(this).html().split('filtro_data')[1];}
            
            return !~text.indexOf(val);

        }).hide();
       

}

function filtro_datas($rows, de_tratado, ate_tratado){

    $rows.hide().filter(function() {
        var text = $(this).text().split("/")
        var entrega = tratar_data(text)
        
        return (entrega>=de_tratado && entrega<=ate_tratado)
    }).show();
   

}




$(document).ready(function() {
    
    var $rows = $('#tabela tbody tr');
    
    $('#filtro').keyup(function() {
        var val = $.trim($(this).val()).replace(/ +/g, ' ').toLowerCase();
        filtro_normal($rows, val)
    });

    $('#mostrar_compra').click(function() {
        var val = "compras"
        
        if ($(this).text()==="Mostrar Compras"){
            $(this).attr('text',"Ocultar Compras")
            $rows.show()
        }
        else {
            $(this).attr('text',"Mostrar Compras")
            $rows.hide().filter(function() {
                var text = $(this).text().replace(/\s+/g, ' ').toLowerCase();
                
                return !~text.indexOf(val);
                
            }).show();
        }
        
    });

    $('#filtro_Mes').change(function() {
        var val = $.trim($(this).val()).replace(/ +/g, ' ').toLowerCase();
        filtro_normal($rows, val, "Filtro_mes")
    });

    $('#filtro_Financeiro').keyup(function() {
     
      procurar_fluxo($rows)  

    });

    $('#data_de_financeiro').change(function() {
            
        procurar_fluxo($rows)
    })

    $('#data_ate_financeiro').change(function() {
            
        procurar_fluxo($rows)
    })

    


    $('#data_de').change(function() {
        var ate = $('#data_ate').val()
        var de = $('#data_de').val()
        if (ate!="" && de!=""){
            
            ate = tratar_data(ate)
            de = tratar_data(de)
            filtro_datas($rows ,de, ate)
            
        } else {
            $rows.show()
        }

    })
    

    $('#data_ate').change(function() {
        var ate = $('#data_ate').val()
        var de = $('#data_de').val()

        if (ate!="" && de!=""){
            
            ate = tratar_data(ate)
            de = tratar_data(de)
            filtro_datas($rows,de, ate)
            
        } else {
            $rows.show()
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


