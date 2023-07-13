$(document).ready(function(){
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

    $('#btn-forgot-password').click(function(e){
        e.preventDefault();
        $('#modal-forgot').click();
        $('#form-reset-password').submit(function(e){
            e.preventDefault();
            $('.on-submit').each(function(){
                $(this).prop('disabled', true);
            })
            let email = $('#email-forgot-input').val();
            $("#email-reset-err").text("");
            const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            $.ajax({
                type: 'POST',
                headers: {"X-CSRFToken": csrftoken,},
                url: $('#form-reset-password').attr('action'),
                data: {'email': email},
                success: function (res) {
                    $('.on-submit').each(function(){
                        $(this).prop('disabled', false);
                    })
                    $('body').html(res['content']);
                },
                error: function (error) {
                    console.log(error.responseJSON);
                    var errorMsg = error.responseJSON;
                    $('.on-submit').each(function(){
                        $(this).prop('disabled', false);
                    })
                    $(`#email-reset-err`).text(errorMsg['msg']);
                }
            })
            });
    });

    $( "#form-submit" ).submit(function(e) {
        e.preventDefault();
        let user = {
            'email' : $("#email").val(),
            'password' : $("#password").val()
        }
        $("#email-err").text("");
        $("#password-err").text("");
        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        $.ajax({
            type: 'POST',
            headers: {"X-CSRFToken": csrftoken,},
            url: window.location.href,
            data: user,
            success: function (res) {
                console.log(res);
                window.location = res['url'];
            },
            error: function (error) {
                console.log(error.responseJSON);
                var errorMsg = error.responseJSON;
                $(`#password-err`).text(errorMsg['message']);
            }
        })

      });
 });