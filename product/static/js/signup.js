$(document).ready(function(){
    // var dis_btn = false;
    var password = "";
    var password2 = "";

    $('#unscore-password').click(function(){
        var passwordInput = $("#password");
        var passwordType = passwordInput.attr("type");
        if (passwordType === "password") {
        passwordInput.attr("type", "text");
        // $(this).text("Hide password");
        } else {
        passwordInput.attr("type", "password");
        // $(this).text("Show password");
        }
    });
    $('#unscore-password2').click(function(){
        var passwordInput = $("#password2");
        var passwordType = passwordInput.attr("type");
        if (passwordType === "password") {
        passwordInput.attr("type", "text");
        // $(this).text("Hide password");
        } else {
        passwordInput.attr("type", "password");
        // $(this).text("Show password");
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
    // $("#close-success").click(function(){
    //     $(".success-checkmark").attr("hidden",true);
    // });
    

    $("#form-submit" ).submit(function(e) {
        e.preventDefault();
        $(".check-icon").hide();
        setTimeout(function () {
          $(".check-icon").show();
        }, 10);
        $("#email-err").text("");
        $("#phone_number-err").text("");
        $("#password-err").text("");
        $("#password2-err").text("");
        let user = {
            'full_name': $('#full_name').val(),
            'email' : $("#email").val(),
            'phone_number' : $("#phone_number").val(),
            'address': $('#address').val(),
            'password' : password,
            'password2': password2
        }
        $('#spinner').addClass('show');
        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        $.ajax({
            type: 'POST',
            headers: {"X-CSRFToken": csrftoken,},
            url: window.location.href,
            data: user,
            success: function (res) {
                console.log(res);
                $('#spinner').removeClass('show');
                $('body').html(res['content']);
                // $(".success-checkmark").removeAttr('hidden');
            },
            error: function (error) {
                $('#spinner').removeClass('show');
                console.log(error.responseJSON);
                var errorMsg = error.responseJSON;
                for (const [key, value] of Object.entries(errorMsg)){
                    $(`#${key}-err`).text(value[0]['message']);
                }

            }
        });
    });

 });