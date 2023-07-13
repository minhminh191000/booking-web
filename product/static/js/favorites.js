function delete_favorite(e, id) {
    e.preventDefault();
    $('#mess-log-order').text('Are you sure you want to delete?');
    $("#mess_log").click();
    $('#mess_icon_fail').prop('hidden', true);
    $('#mess_icon_success').prop('hidden', true);
    $('#btn_confirm_mess').prop('hidden', false);
    $('#btn_confirm_mess2').prop('hidden', true);
    $('#btn_confirm_mess').click(function (e) {
        e.preventDefault();
        let data = {
            'food_id': id
        }
        // console.log(data);
        // console.log(window.location.href);
        const csrftoken = $('[name=csrfmiddlewaretoken]').val();
        $.ajax({
            type: 'POST',
            headers: { "X-CSRFToken": csrftoken, },
            url: window.location.href,
            data: data,
            success: function (res) {
                console.log(data);
                $('#mess-log-order').text('Delete successful!');
                $('#btn_confirm_mess').prop('hidden', true);
                $('#btn_confirm_mess2').prop('hidden', false);
                $('#mess_icon_success').prop('hidden', false);
                $('#btn_confirm_mess2').click(function (e) {
                    location.reload();
                });
                $("#btn-close-mess").click(function (e) {
                    location.reload();
                });

            },
            error: function (error) {
                $('#mess-log-order').text("Delete failed!");
                $('#btn_confirm_mess').prop('hidden', true);
                $('#btn_confirm_mess2').prop('hidden', false);
                $('#mess_icon_success').prop('hidden', true);
                $('#mess_icon_fail').prop('hidden', false);
            }
        })
    })
}
let food_add = { 'quantity': 1 }
function addToTable(id, img, name, price, is_order) {
    if (is_order) {
        if (is_order == 'True') {
            food_add['food_id'] = id;
            $('#food_add_url').attr('src', img);
            $('#food_add_url').attr('alt', "img");
            $('#food_add_name').text(name);
            $('#food_add_price').text(`${price} vnđ`);
            $('#add_log').click();
        }
        else {
            $('#mess-log-order').text("In future, You haven't any orders.");
            $('#mess_log').click();
        }
    }
    else {
        $('#login-require').click();
    }
}
function subQuantity() {
    let quantity = parseInt($('#food_add_quantity').text());
    if (quantity > 1) {
        food_add['quantity'] = quantity - 1;
        $('#food_add_quantity').text(quantity - 1);
    }
}
function addQuantity() {
    let quantity = parseInt($('#food_add_quantity').text());
    food_add['quantity'] = quantity + 1;
    $('#food_add_quantity').text(quantity + 1);
}
function submitAdd() {
    $('.on-submit').each(function () {
        $(this).prop('disabled', true);
    });
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    food_add['order_id'] = parseInt($('#select-ordered').val());
    $.ajax({
        type: 'POST',
        headers: {
            "X-CSRFToken": csrftoken,
        },
        url: $('#btn_confirm_add').attr('url'),
        data: food_add,
        success: function (response) {
            $('.on-submit').each(function () {
                $(this).prop('disabled', false);
            });
            $('#btn_confirm_mess').prop('hidden', true);
            $('#btn_confirm_mess2').prop('hidden', false);
            $('#mess-log-order').text("Add successfully!");
            $('#close-add').click();
            $('#mess_log').click();
            $('#mess_icon_fail').prop('hidden', true);
            $('#mess_icon_success').prop('hidden', false);
        },
        error: function (response) {
            $('.on-submit').each(function () {
                $(this).prop('disabled', false);
            });
            $('#btn_confirm_mess').prop('hidden', true);
            $('#btn_confirm_mess2').prop('hidden', false);
            // console.log(response.responseJSON);
            $('#mess-log-order').text(response.responseJSON['msg']);
            $('#close-add').click();
            $('#mess_log').click();
            $('#mess_icon_success').prop('hidden', true);
            $('#mess_icon_fail').prop('hidden', false);


        }
    })
}

$(document).ready(function () {

});