function handleComment(id){
    let data = {
        'food_id': id,
    };
    $('input[name="rate"]').each(function() {
        if ($(this).is(':checked')) {
        data['rating'] = parseInt($(this).val());
        }
    });
    data['comment'] = $('#comment-input').val();
    // console.log(data);
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    // console.log(csrftoken);
    $.ajax({
        type: 'POST',
        headers: { 
            "X-CSRFToken": csrftoken,
        },
        url: window.location.href,
        data: data,
        success: function (response) {
            location.reload();
        },
        error: function(response){
            console.log(response);
        }
    });
}
function handleHelpful(e, name,id){
    e.preventDefault();
    let data = {
        'id': id,
        'category': name,
    }
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    $.ajax({
        type: 'POST',
        headers: { 
            "X-CSRFToken": csrftoken,
        },
        url:$(`#${name}-${id}`).attr('href') ,
        data: data,
        success: function (response) {
            $(`#value-${name}-${id}`).text(response[name]); 
            
        },
        error: function(response){
            console.log(response);
            
        }
    });
    if ($(`#${name}-${id}`).attr('name') === '1') {
        $(`#${name}-${id}`).attr('name','-1');
    } else {
        $(`#${name}-${id}`).attr('name','1');
    }
    // console.log(name,$(`#${name}-${id}`).attr('name'));
}
let food_add = {'quantity':1}
function addToTable(id,img,name,price, is_order){
    if (is_order){
        if (is_order == 'True'){
            food_add['food_id'] = id;
            $('#food_add_url').attr('src',img);
            $('#food_add_url').attr('alt',"img");
            $('#food_add_name').text(name);
            $('#food_add_price').text(`${price} vnđ`);
            $('#add_log').click();
        }
        else{
            $('#mess-log-order').text("In future, You haven't any orders.");
            $('#mess_log').click();
        }
    }
    else{
        $('#login-require').click();
    }
}
function subQuantity(){
    let quantity = parseInt($('#food_add_quantity').text());
    if (quantity>1){
        food_add['quantity'] = quantity - 1;
        $('#food_add_quantity').text(quantity - 1);
    }
}
function addQuantity(){
    let quantity = parseInt($('#food_add_quantity').text());
    food_add['quantity'] = quantity + 1;
    $('#food_add_quantity').text(quantity + 1);
}
function submitAdd(){
    $('#btn_confirm_add').prop('disabled', true);
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
            $('#btn_confirm_add').prop('disabled', false);
            $('#mess-log-order').text("Add successfully!");
            $('#close-add').click();
            $('#mess_log').click();
            $('#mess_icon_fail').prop('hidden', true);
            $('#mess_icon_success').prop('hidden', false);
        },
        error: function(response){
            $('#btn_confirm_add').prop('disabled', false);
            // console.log(response.responseJSON);
            $('#mess-log-order').text(response.responseJSON['msg']);
            $('#close-add').click();
            $('#mess_log').click();
            $('#mess_icon_success').prop('hidden', true);
            $('#mess_icon_fail').prop('hidden', false);

            
        }
    })
}
$(document).ready(function() {
    $('#add-favorite').click(function(e) {
        e.preventDefault();
        var url = document.getElementById('add-favorite').getAttribute('url');
        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        var id = window.location.pathname.substring(window.location.pathname.lastIndexOf('/') + 1);
        // console.log(csrftoken);
        var btn = $('#add-favorite');
        btn.prop('disabled', true);
        btn.toggleClass('no-drop');
        $.ajax({
            type: 'POST',
            headers: { 
                "X-CSRFToken": csrftoken,
            },
            url: url,
            data: {"food_id":id},
            success: function (response) {
                console.log(response); 
                btn.prop('disabled', false);
                btn.toggleClass('no-drop');
                $('#icon-favorite').toggleClass('fa-solid');
                $('#quantity-favorite').text(response['quantity']);
            },
            error: function(response){
                console.log(response);
                if (response.status==401){
                    $('#login-require').click();
                }
                btn.prop('disabled', false);
                btn.toggleClass('no-drop');
            }
        });
        
    });
});