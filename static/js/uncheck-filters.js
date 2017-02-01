function uncheckFilters() {
    $('input[type="checkbox"]:checked').prop('checked',false);
    $('input:text').val('');
    $('.loading-icon').css('opacity', '1');
    submit();
}