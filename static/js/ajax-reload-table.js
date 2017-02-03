var timer;
var form = $('#auto-submit-form');
var delay = form.attr('data-submit-delay');
$(document).ready(function submit(e) {
    $('.clickable').bind('click keydown', function(){
        var submitForm = $('#auto-submit-form');
        clearTimeout(timer);
        $('.loading-icon').css('opacity','1');
        timer = setTimeout(function(){
            ajax_setup();
        }, delay);
    });
    $('input[type=radio]').bind('click', function() {
        var submitForm = $('#auto-submit-form');
        ajax_setup();
    })
});

$(document).ajaxComplete(function submit(e) {
    $('.clickable').bind('click keydown', function(){
        var submitForm = $('#auto-submit-form');
        clearTimeout(timer);
        $('.loading-icon').css('opacity','1');
        timer = setTimeout(function(){
            ajax_setup();
        }, delay);
    });
    $('input[type=radio]').bind('click', function() {
        var submitForm = $('#auto-submit-form');
        ajax_setup();
    })
});

function ajax_setup() {
    make_request();
};

function gatherEmployeeFilters() {
    return {
        order: $('input[name=order]:checked', '#auto-submit-form').val(),
        employee_filter: $('#employee_filter').val(),
        position_sale: $('input[name=position_sale]:checked').val(),
        position_other: $('input[name=position_other]:checked').val(),
        position_production: $('input[name=position_production]:checked').val(),
        hide_paid_employees_filter: $('input[name=hide_paid_employees_filter]:checked').val(),
        hide_zero_salary_months: $('input[name=hide_zero_salary_months]:checked').val(),
        per_page: $('select[name=per_page]').val(),
        page: $('input[name=pg]:checked').val(),
    }
}

function make_request() {
    try {
        var params = gatherEmployeeFilters();
    }
    catch(err) {
        var params = gatherMonthFilters();
    }
    $.get({
        url: '',
        data: params,
        dataType: "html",
        success: function(content) {
            $(".ajax-loader").replaceWith(content);
            $(".loading-icon").css("opacity", "0");
            if(content.indexOf('<p>') !== -1) {
                var template = $('#hidden-template').html();
                $('#msg').replaceWith(template);
            } else {
                $('#msg').replaceWith('<div id="msg"></div>');
            }
        }
    });
    
}
