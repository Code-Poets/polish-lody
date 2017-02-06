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
    var params = gatherFilters();
    $.get({
        url: '',
        data: params,
        dataType: "html",
        success: function(content) {
            $(".ajax-loader").replaceWith(content);
            $(".loading-icon").css("opacity", "0");
            console.log('great success');
            if(content.indexOf('<p>') !== -1) {
                console.log('wtf');
                var template = $('#hidden-template').html();
                $('#msg').replaceWith(template);
            } else {
                $('#msg').replaceWith('<div id="msg"></div>');
            }
        }
    });
    
}
