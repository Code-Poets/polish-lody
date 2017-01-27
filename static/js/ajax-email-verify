function ajaxVerify() {
    var verifyemail = $('#id_email').val();
    $.ajax({
        url: 'new/emailverify',
        data: {data: verifyemail},
        type: "GET",
        success: function(response) {
            if(response.status === 1) {
                $('.verify-email').show(500);
                $('#id_email').addClass('already-exists')
            }
            else {
                $('.verify-email').hide(500);
                $('#id_email').removeClass('already-exists')
            }
        }
    });
}

var timer;
$('#id_email').keyup(function() {
    clearTimeout(timer);
    timer = setTimeout(function() {
        ajaxVerify();
    }, 500)
})