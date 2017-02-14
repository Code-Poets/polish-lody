var timer;
var form = $('#auto-submit-form');
var delay = form.attr('data-submit-delay');
$(document).ready(function submit(e) {
    $('.clickable').bind('click keydown', function(){
        var submitForm = $('#auto-submit-form');
        clearTimeout(timer);
        $('.loading-icon').css('opacity','1');
        timer = setTimeout(function(){
            make_request();
        }, delay);
    });
    $('input[type=radio]').bind('click', function() {
        clearTimeout(timer);
        $('.loading-icon').css('opacity','1');
        var submitForm = $('#auto-submit-form');
        make_request();
    })
});

$(document).ajaxComplete(function submit(e) {
    $('.clickable').bind('click keydown', function(){
        var submitForm = $('#auto-submit-form');
        clearTimeout(timer);
        $('.loading-icon').css('opacity','1');
        timer = setTimeout(function(){
            make_request();
        }, delay);
    });
    $('input[type=radio]').bind('click', function() {
        clearTimeout(timer);
        $('.loading-icon').css('opacity','1');
        var submitForm = $('#auto-submit-form');
        make_request();
    })
});

function ajax_setup() {
    $('input[type=radio]').bind('click', function() {
        clearTimeout(timer);
        var submitForm = $('#auto-submit-form');
        make_request();
    })
};

function make_request() {
    try {
        var params = gatherFilters();
    } 
    catch(err) {
        var params = { };
    }
    $.ajax({
        url: '',
        data: params,
        dataType: "html",
        method: "GET",
        timeout: 5000,
        success: function(content) {
            $(".ajax-loader").replaceWith(content);
            $(".loading-icon").css("opacity", "0");
            if(content.indexOf('<p>') !== -1) {
                var errTemplate = $('#hidden-template').html();
                $('#msg').replaceWith(errTemplate);
            } else {
                $('#msg').replaceWith('<div id="msg"></div>');
            }
        }
    }).fail(function(jqXHR){
        $(".loading-icon").css("opacity", "0");
        ajaxErrorHandler(jqXHR);
    });
}
function ajaxErrorHandler(jqXHR) {
    if (jqXHR.status === 500) {
        var errTemplate = ('<div class="alert alert-warning alert-dismissable" id="msg">' + 
            '<button type="button" class="close" data-dismiss="alert" aria-hidden="true">×</button>' + 
            '<span>An internal server error occurred. If the issue persists, contact system administrator.</span></div>');
    } else if (jqXHR.status === 404) {
        var errTemplate = ('<div class="alert alert-warning alert-dismissable" id="msg">' + 
            '<button type="button" class="close" data-dismiss="alert" aria-hidden="true">×</button>' + 
            '<span>It seems that you tried to access something that does not exist.</span></div>');
    } else {
        var errTemplate = ('<div class="alert alert-warning alert-dismissable" id="msg">' + 
            '<button type="button" class="close" data-dismiss="alert" aria-hidden="true">×</button>' + 
            '<span>An unexpected error occurred.</span></div>');
    }
    $('#msg').replaceWith(errTemplate);
}

