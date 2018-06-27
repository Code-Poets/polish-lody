function makePerPageActive(e) {
    var num = $('select[name=per_page]').val();
    $('.page-no').removeClass('active');
    $('#per-page-' + num).addClass('active');
};

$(document).ready(function(e) {
    makePerPageActive(e);
});