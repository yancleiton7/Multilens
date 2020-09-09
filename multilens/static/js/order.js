$(document).ready(function () {
    $("td > a").bind("click", function () {
        var item = $(this).parent().parent()
        $.ajax({
            url: window.location.href + '?item_id=' + item.attr('item_id'),
            type: "DELETE",
            success: function () {
                item.remove();
            },
            fail: function () {
                alert("Não foi possível excluir o item, tente novamente mais tarde");
            },
            error: function () {
                alert("Não foi possível excluir o item, tente novamente mais tarde");
            }
        })
    });

    $(".add-item").bind("click", function () {
        $.ajax({
            url: window.location.href,
            type: "PUT",
            contentType: "application/json; charset=utf-8",
            data: JSON.stringify({
                amount: $("#amount").val(),
                item_id: $("#product").val(),
            }),
            success: function (response) {
                if (response.success) {
                    location.reload();
                }
                else {
                    alert(response.message)
                }
            },
            fail: function () {
                alert("Não foi possível adicionar o item, tente novamente mais tarde");
            },
            error: function () {
                alert("Não foi possível adicionar o item, tente novamente mais tarde");
            }
        })
    });

    $("#register").change(function () {
        $.ajax({
            url: window.location.origin + "/api/register/" + $("#register").val(),
            type: "GET",
            success: function(response){
                $("#address").val(response.address),
                $("#zip").val(response.zip),
                $("#district").val("Distrito"),
                $("#city").val(response.city)
            }
        })
    })
});