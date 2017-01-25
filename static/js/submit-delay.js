var timer;
var form = $('#auto-submit-form');
var delay = form.attr('data-submit-delay');
$(document).ready(function(e) {
    $('.clickable').bind('click keydown', function(){
        var $submitForm = $('#auto-submit-form');
        clearTimeout(timer);
        $('.loading-icon').css('opacity','1');
        timer = setTimeout(function(){
            $submitForm.submit();
        }, delay);
    });
});