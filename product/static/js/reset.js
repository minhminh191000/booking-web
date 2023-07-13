$(document).ready(function() {
    var password = "";
    var password2 = "";

    $('#unscore-password').click(function(){
        var passwordInput = $("#password");
        var passwordType = passwordInput.attr("type");
        if (passwordType === "password") {
        passwordInput.attr("type", "text");
        } else {
        passwordInput.attr("type", "password");
        }
    });
    $('#unscore-password2').click(function(){
        var passwordInput = $("#password2");
        var passwordType = passwordInput.attr("type");
        if (passwordType === "password") {
        passwordInput.attr("type", "text");
        } else {
        passwordInput.attr("type", "password");
        }
    });
    $('#password').on('input', function(){
        password = $('#password').val();
        $('#signup').prop('disabled', true);
        if (password.length <8) {
            $('#password-err').text('Password must be at least 8 characters');
        }else{
            if(password == password2){
                $('#signup').prop('disabled', false);
            }
            $('#password-err').text('');
            $('#password2-err').text('');
        }
    });
    $('#password2').on('input', function(){
        password2 = $('#password2').val();
        $('#signup').prop('disabled', true);
        if(password != password2) {
            $('#password2-err').text('Password does not match');
        }else{
            $('#signup').prop('disabled', false);
            $('#password2-err').text('');
            $('#password-err').text('');
        }
    });

    $("#form-submit" ).submit(function(e) {
        e.preventDefault();
        $("#password-err").text("");
        $("#password2-err").text("");
        let user = {
            'payload': $("#form-submit").attr('value'),
            'password' : password,
            'password2': password2
        }
        console.log(user);
        $('#spinner').addClass('show');
        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        $.ajax({
            type: 'POST',
            headers: {"X-CSRFToken": csrftoken,},
            url: window.location.href,
            data: user,
            success: function (res) {
                console.log(res);
                $('#mess_log').click();
                $('#btn_confirm_mess').click(function(){
                    location.href= $('#btn_confirm_mess').attr('url');
                });
            },
            error: function (error) {
                console.log(error.responseJSON);
                var errorMsg = error.responseJSON;
                for (const [key, value] of Object.entries(errorMsg)){
                    $(`#${key}-err`).text(value[0]['message']);
                }

            }
        });
    });
});