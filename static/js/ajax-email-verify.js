function ajaxVerify() {
    var verifyemail = $('#id_email').val();
    $.ajax({
        url: 'new/emailverify',
        data: {data: verifyemail},
        type: "GET",
        success: function(response) {
            if(response.status === 1) {
                $('.verify-email').show(500);
                $('#id_email').addClass('already-exists');
                $('input[name=submit]').attr('disabled', true);
                $('#id_email').attr('data-toggle', 'popover')
                $('#id_email').attr('data-placement', 'bottom');
                $('#id_email').attr('data-content', 'This e-mail address is already used.');
                $('#id_email').popover('show');
            }
            else {
                $('input[name=submit]').attr('disabled', false);
                $('.verify-email').hide(500);
                $('#id_email').removeClass('already-exists');
                $('#id_email').popover('hide');
            }
        }
    });
}

$('#id_password2').focusout(function() {
    var pass1 = $('#id_password1').val();
    var pass2 = $('#id_password2').val();
    if( pass1 !== pass2 ) {
        $('input[name=submit]').attr('disabled', true);
        $('#id_password2').attr('data-toggle', 'popover');
        $('#id_password2').attr('data-placement', 'bottom');
        $('#id_password2').attr('data-content', 'Passwords do not match.');
        $('#id_password1').addClass('already-exists');
        $('#id_password2').addClass('already-exists');
        $('#id_password2').popover('show');

    } else if ( pass1 === pass2 ) {
        $('input[name=submit]').attr('disabled', false);
        $('#id_password2').attr('data-toggle', false);
        $('#id_password2').attr('data-placement', false);
        $('#id_password2').attr('data-content', false);
        $('#id_password1').removeClass('already-exists');
        $('#id_password2').removeClass('already-exists');
        $('#id_password2').popover('hide');
    }
})

$('#id_first_name').focusout(function() {
    var input = $('#id_first_name').val();
    if ( input === '') {
        $('#id_first_name').attr('data-toggle', 'popover');
        $('#id_first_name').attr('data-placement', 'bottom');
        $('#id_first_name').attr('data-content', 'This field is required.');
        $('#id_first_name').popover('show');
    } else {
        $('#id_first_name').attr('data-toggle', false);
        $('#id_first_name').attr('data-placement', false);
        $('#id_first_name').attr('data-content', false);
        $('#id_first_name').popover('hide');
    }
});
$('#id_last_name').focusout(function() {
    var input2 = $('#id_first_name').val();
    if ( input2 === '') {
        $('#id_last_name').attr('data-toggle', 'popover');
        $('#id_last_name').attr('data-placement', 'bottom');
        $('#id_last_name').attr('data-content', 'This field is required.');
        $('#id_last_name').popover('show');
    } else {
        $('#id_last_name').attr('data-toggle', false);
        $('#id_last_name').attr('data-placement', false);
        $('#id_last_name').attr('data-content', false);
        $('#id_last_name').popover('hide');
    }
});
$(document).ready(function() {
    $('[data-toggle="popover"]').popover();
});

var timer;
$('#id_email').on('change blur keyup input', function() {
    clearTimeout(timer);
    timer = setTimeout(function() {
        ajaxVerify();
    }, 500)
})
