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

function ajaxVerifyDate() {
    var verify_year = $('#id_year').val();
    var verify_month = $('#id_month').val();
    var month_text = $('#id_month :selected').text();
    var employee_id = getPk();
    if(verify_year == yearinit && verify_month == monthinit){
        $('input[name=submit]').attr('disabled', false);
        $('#id_year').removeClass('already-exists');
        $('#id_month').removeClass('already-exists');
        $('#id_year').removeAttr('data-toggle');
        $('#id_year').removeAttr('data-placement');
        $('#id_year').removeAttr('data-content');
        $('#id_year').popover('hide');
        return ;
    } else {
        $.ajax({
            url: '../../employees/dateverify/',
            data: {year: verify_year,
                    month: verify_month,
                    employee_id: employee_id
                    },
            type: "GET",
            success: function(response) {
                if(response.is_date) {
                    $('#id_year').addClass('already-exists');
                    $('#id_month').addClass('already-exists');
                    $('input[name=submit]').attr('disabled', true);
                    $('#id_year').attr('data-toggle', 'popover')
                    $('#id_year').attr('data-placement', 'right');
                    $('#id_year').attr('data-content',month_text +' '+ verify_year +' already exists.');
                    $('#id_year').popover('show');
                }
                else {
                    $('input[name=submit]').attr('disabled', false);
                    $('#id_year').removeClass('already-exists');
                    $('#id_month').removeClass('already-exists');
                    $('#id_year').removeAttr('data-toggle');
                    $('#id_year').removeAttr('data-placement');
                    $('#id_year').removeAttr('data-content');
                    $('#id_year').popover('hide');
                }
            }
        });
    }
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
// $(document).ready(function() {
//     $('[data-toggle="popover"]').popover();
// });

var timer;
$('#id_email').on('change blur keyup input', function() {
    clearTimeout(timer);
    timer = setTimeout(function() {
        ajaxVerify();
    }, 500)
});

$('#id_year').change(function(){
    ajaxVerifyDate();
});

$('#id_month').change(function(){
    ajaxVerifyDate();
});