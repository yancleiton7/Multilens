

function sortTable(n) {
    var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
    table = document.getElementById("tabela");
    switching = true;
    
    //Set the sorting direction to ascending:
    dir = "asc"; 

    rows = table.rows;

    nome_titulo = rows[0].getElementsByTagName("TH")[n].innerHTML.toLowerCase()
    

    /*Make a loop that will continue until
    no switching has been done:*/
    while (switching) {
      //start by saying: no switching is done:
      switching = false;
      rows = table.rows;
      /*Loop through all table rows (except the
      first, which contains table headers):*/
      for (i = 1; i < (rows.length - 1); i++) {
        //start by saying there should be no switching:
        shouldSwitch = false;
        /*Get the two elements you want to compare,
        one from current row and one from the next:*/

        x = rows[i].getElementsByTagName("TD")[n];
        y = rows[i + 1].getElementsByTagName("TD")[n];
        /*check if the two rows should switch place,
        based on the direction, asc or desc:*/

        /*Extract text of object */
        valor_de_x = x.innerHTML.toLowerCase()
        valor_de_y = y.innerHTML.toLowerCase()

        /*Verificar se é data ou dinheiro*/
        
        verifica_valor = valor_de_x.slice(0,5)
        if (verifica_valor.includes("r$ ",0)){
            
            valor_de_x = parseFloat(valor_de_x.split("r$ ")[1].replace(",","."))
            valor_de_y = parseFloat(valor_de_y.split("r$ ")[1].replace(",","."))
            

        } else if (verifica_valor.includes("/",2)){
            
            valor_de_x = tratar_data(valor_de_x, "/")
            valor_de_y = tratar_data(valor_de_y, "/")
            

        } else if (nome_titulo==="id" || nome_titulo==="disponível" || nome_titulo==="estoque mínimo"){
            
            valor_de_x = parseInt(valor_de_x)
            valor_de_y = parseInt(valor_de_y)
            

        }





        if (dir == "asc") {
          if (valor_de_x > valor_de_y) {
            //if so, mark as a switch and break the loop:
            shouldSwitch= true;
            break;
          }
        } else if (dir == "desc") {
          if (valor_de_x < valor_de_y) {
            //if so, mark as a switch and break the loop:
            shouldSwitch = true;
            break;
          }
        }
      }
      if (shouldSwitch) {
        /*If a switch has been marked, make the switch
        and mark that a switch has been done:*/
        rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
        switching = true;
        //Each time a switch is done, increase this count by 1:
        switchcount ++;      
      } else {
        /*If no switching has been done AND the direction is "asc",
        set the direction to "desc" and run the while loop again.*/
        if (switchcount == 0 && dir == "asc") {
          dir = "desc";
          switching = true;
        }
      }
    }
  }



function tratar_data(data, item_split="-"){
    var data_tratada = data.split(item_split)

    if (item_split==="-"){
        data_tratada = parseInt(data_tratada[0]+""+data_tratada[1]+""+data_tratada[2])
    } else {
        var data_tratada = parseInt(data_tratada[2].slice(0,4)+""+data_tratada[1].slice(-2)+""+data_tratada[0].slice(-2))
    }
    
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
        var data = $(this).text()
        var data_tratada = tratar_data(data, "/")

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
        var text = $(this).text()
        
        var entrega = tratar_data(text, "/")
        
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

    $('#box_entrada').click(function() {
        
        $('#filtro_Financeiro').val('Entrada')    
        procurar_fluxo($rows)
    })  

    $('#box_saida').click(function() {
        
        $('#filtro_Financeiro').val('Saida')    
        procurar_fluxo($rows)
    })  

    $('#box_total').click(function() {
        
        $('#filtro_Financeiro').val('')    
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

    $('#quantidade_linhas_tabela').change(function() {
        quantidade = $(this).find(":selected").text()

        caminho = window.location.href.split('?')[0]
        if (caminho.length===1){
            window.location.href = window.location.href+'?limit='+quantidade
        } else {
            window.location.href = caminho+'?limit='+quantidade
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


