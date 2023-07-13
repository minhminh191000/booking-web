var is_change_avatar = false;
var img = null;
var loadFile = function (event) {
    var image = document.getElementById("output");
    image.src = URL.createObjectURL(event.target.files[0]);
    img = event.target.files[0];
    is_change_avatar = true;
};

$(document).ready(function () {
    $('#unscore-password').click(function () {
        var passwordInput = $("#pass-input");
        var passwordType = passwordInput.attr("type");
        if (passwordType === "password") {
            passwordInput.attr("type", "text");
            // $(this).text("Hide password");
        } else {
            passwordInput.attr("type", "password");
            // $(this).text("Show password");
        }
    });
    $('#unscore-password2').click(function () {
        var passwordInput = $("#pass2-input");
        var passwordType = passwordInput.attr("type");
        if (passwordType === "password") {
            passwordInput.attr("type", "text");
            // $(this).text("Hide password");
        } else {
            passwordInput.attr("type", "password");
            // $(this).text("Show password");
        }
    });

    $('#form-update-user').submit(async function (e) {
        e.preventDefault();
        $(".on-submit").each(function() {
            $(this).prop('disabled', true);
        });
        let full_name = $('#name-input').val();
        let email = $('#email-input').val();
        let phone = $('#phone-input').val();
        let address = $('#address-input').val();
        let password = $('#pass-input').val();
        let password2 = $('#pass2-input').val();
        let data_user = {
            'full_name': full_name,
            'email': email,
            'phone_number': phone,
            'address': address,
            'url_img': $("#output").attr('src')
        }
        if (password.length != password2.length) {
            $('#mess-log-order').text("Password does not match");
            $('#btn_confirm_mess').prop('hidden', true);
            $('#btn_confirm_mess2').prop('hidden', false);
            $("#mess_log").click();
            $('#mess_icon_success').prop('hidden', true);
            $('#mess_icon_fail').prop('hidden', false);
        }
        else {
            if (password){
                data_user['password'] = password
                data_user['password2'] = password2
            }
            if (is_change_avatar) {
                var fd = new FormData();
                fd.append('image', img);
                var settings = {
                    "url": "https://api.imgbb.com/1/upload?key=0b4ad03dd615619b2ce49b6fa5af3a09",
                    "method": "POST",
                    "timeout": 0,
                    "processData": false,
                    "mimeType": "multipart/form-data",
                    "contentType": false,
                    "data": fd
                };
                await $.ajax(settings).done(function (response) {
                    var jx = JSON.parse(response);
                    console.log(jx.data.url);
                    data_user['url_img'] = jx.data.url;
                });
            }
            const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            $.ajax({
                type: 'POST',
                headers: { "X-CSRFToken": csrftoken, },
                url: window.location.href,
                data: { 'data_user': JSON.stringify(data_user) },
                success: function (res) {
                    $('#mess-log-order').text('Update successful!');
                    $("#mess_log").click();
                    $('#mess_icon_fail').prop('hidden', true);
                    $('#mess_icon_success').prop('hidden', false);
                    // console.log(data_user);
                    $(".on-submit").each(function() {
  $(this).prop('disabled', false);
});
                    $('#btn_confirm_mess').click(function(e){
                        location.reload();
                    })
                },
                error: function (error) {
                    let msg = error.responseJSON['msg'];
                    console.log(msg);
                    $('#mess-log-order').text(msg);
                    $('#btn_confirm_mess').prop('hidden', true);
                    $('#btn_confirm_mess2').prop('hidden', false);
                    $("#mess_log").click();
                    $(".on-submit").each(function() {
  $(this).prop('disabled', false);
}); 
                    $('#mess_icon_success').prop('hidden', true);
                    $('#mess_icon_fail').prop('hidden', false);
                }
            })
        }
    });
});
