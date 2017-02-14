function ajaxVerify() {
    var verifyemail = $('#id_email').val();
    $.post({
        url: 'new/emailverify/',
        data: {
            email: verifyemail,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            },
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
                $('#id_email').removeAttr('data-toggle')
                $('#id_email').removeAttr('data-placement');
                $('#id_email').removeAttr('data-content')
                $('.verify-email').hide(500);
                $('#id_email').removeClass('already-exists');
                $('#id_email').popover('hide');
            }
        },
        error: function(thrownError) {
            console.log(thrownError);
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
        $('#id_password2').removeAttr('data-toggle');
        $('#id_password2').removeAttr('data-placement');
        $('#id_password2').removeAttr('data-content');
        $('#id_password1').removeClass('already-exists');
        $('#id_password2').removeClass('already-exists');
        $('#id_password2').popover('hide');
    }
})
$(document).ready(function() {
    $('#id_first_name').on('blur', function() {
        var f_name = $('#id_first_name').val();
        if ( f_name === '') {
            $('#id_first_name').attr('data-toggle', 'popover');
            $('#id_first_name').attr('data-placement', 'bottom');
            $('#id_first_name').attr('data-content', 'This field is required.');
            $('#id_first_name').popover('show');
        } else {
            $('#id_first_name').removeAttr('data-toggle');
            $('#id_first_name').removeAttr('data-placement');
            $('#id_first_name').removeAttr('data-content');
            $('#id_first_name').popover('hide');
        }
    });
});
$(document).ready(function() {
    $('#id_last_name').on('blur', function() {
        var l_name = $('#id_last_name').val();
        if ( l_name === '') {
            $('#id_last_name').attr('data-toggle', 'popover');
            $('#id_last_name').attr('data-placement', 'bottom');
            $('#id_last_name').attr('data-content', 'This field is required.');
            $('#id_last_name').popover('show');
        } else {
            $('#id_last_name').attr('data-toggle', '');
            $('#id_last_name').attr('data-placement', '');
            $('#id_last_name').attr('data-content', '');
            $('#id_last_name').popover('hide');
        }
    });
});

var timer;
$('#id_email').on('change blur keyup input', function() {
    clearTimeout(timer);
    timer = setTimeout(function() {
        ajaxVerify();
    }, 500)
})
