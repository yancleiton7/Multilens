function add_item() {
    $.ajax({
        url: window.location.href,
        type: "POST",
        dataType: 'json',
        contentType: 'application/json',
        data: JSON.stringify({
            items:
            {
                id: $("#product option:selected").val(),
                amount: $("#amount").val()
            }
        }),
    })
}

function remove_item(item_id) {
    $.ajax({
        url: window.location.href + '?item_id=' + item_id,
        type: "DELETE"
    })
}

$(document).ready(function () {
    $("td > a").bind("click", function () {
        $.ajax({
            url: window.location.href + '?item_id=' + $(this).parent().parent().attr('item_id'),
            type: "DELETE",
        })
        $(this).parent().parent().remove()
    });
}); 