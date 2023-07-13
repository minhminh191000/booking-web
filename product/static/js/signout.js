$(document).ready(function(){
    $("#signout-btn").click(function(e){
        e.preventDefault();
        $('#mess-log-order').text('Do you want to sign out?');
        $("#mess_log").click();
        $('#mess_icon_fail').prop('hidden', true);
        $('#mess_icon_success').prop('hidden', true);
        $('#btn_confirm_mess').click(function(e){
            window.location.href = $("#signout-btn").attr('href');
        })
    });
});