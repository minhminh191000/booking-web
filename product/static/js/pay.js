let pay_discount = {};

function setBill(id){
    pay_discount[id]= $(`#select-${id}`).find('option:selected').attr('name');
    let discount = parseInt($(`#select-${id}`).val());
    let old_money = parseFloat($(`#need-pay-${id}`).text().replace(' vnd',''));
    let new_money = (old_money-old_money*(discount)/100)*1000;
    new_money = new Intl.NumberFormat("de-DE").format(new_money);
    $(`#${id}-total`).text(`${new_money} vnd`);
}
function submitPay(id){
    let pay = {
        'id': id,
    }
    if (pay_discount[id]){
        pay['discount'] = pay_discount[id];
    }
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    $.ajax({
        type: 'POST',
        headers: {"X-CSRFToken": csrftoken,},
        url: window.location.href,
        data: pay,
        success:  function (response) {
            $('#mess-log-order').text('Pay successful!');
            $("#mess_log").click();
            $('#mess_icon_fail').prop('hidden', true);
            $('#mess_icon_success').prop('hidden', false);
            $('#btn_confirm_mess').click(function(e){
                e.preventDefault();
                location.reload();
            });
            $('#btn-close-mess').click(function(e){
                e.preventDefault();
                location.reload();
            });
        },
        error: function(error){
            let msg = error.responseJSON['msg'];
            console.log(msg);
            $('#mess-log-order').text(msg);
            $('#btn_confirm_mess').prop('hidden', true);
            $('#btn_confirm_mess2').prop('hidden', false);
            $("#mess_log").click();
            $('#mess_icon_success').prop('hidden', true);
            $('#mess_icon_fail').prop('hidden', false);
        }
    });
}