var timer;
var form = $('#auto-submit-form');
var delay = form.attr('data-submit-delay');
$(document).ready(function submit(e) {
    $('.clickable').bind('click keydown', function () {
        clearTimeout(timer);
        $('.loading-icon').css('opacity', '1');
        timer = setTimeout(function () {
            try {
                var parameters = gatherFilters();
                // delete parameters.page;
            }
            catch (err) {
                var parameters = {};
            }
            makeRequest(parameters);
        }, 100);
    });
    $('input[name=order], input[name=pg]').bind('click', function () {
        try {
            var parameters = gatherFilters();
        }
        catch (err) {
            var parameters = {};
        }
        $('.loading-icon').css('opacity', '1');
        makeRequest(parameters);
    })
    $('.reset-filters').bind('click', function () {
        uncheckFilters(timer);
    });
});

$(document).ajaxComplete(function submit(e) {
    $('.clickable').bind('click keydown', function () {
        clearTimeout(timer);
        $('.loading-icon').css('opacity', '1');
        timer = setTimeout(function () {
            try {
                var parameters = gatherFilters();
                delete parameters.page;
            }
            catch (err) {
                var parameters = {};
            }
            makeRequest(parameters);
        }, delay);
    });
    $('input[name=order], input[name=pg]').bind('click', function () {
        try {
            var parameters = gatherFilters();
        }
        catch (err) {
            var parameters = {};
        }
        clearTimeout(timer);
        $('.loading-icon').css('opacity', '1');
        makeRequest(parameters);
    });
    $('.reset-filters').bind('click', function () {
        uncheckFilters(timer);
    });
});

function ajaxSetup() {
    $('input[type=radio]').bind('click', function () {
        clearTimeout(timer);
        makeRequest();
    })
};

$(document).ready(function () {
    $('.chkbx').click(function () {
        $('.chkbx').toggleClass('glyphicon-remove');
        $('.chkbx').toggleClass('glyphicon-ok');
    })
})

function uncheckFilters(timer) {
    clearTimeout(timer)
    $('input[type="checkbox"]:checked').prop('checked', false);
    $('input:text').val('');
    $('input:text').attr('placeholder', '');
    $('.loading-icon').css('opacity', '1');
    $('.page-no').removeClass('active');
    $('#per-page-10').addClass('active');
    makeRequest();
}

function makeRequest(parameters) {
    console.log('Start makeRequest');


    $.ajax({
        url: '',
        data: parameters,
        dataType: "html",
        method: "GET",
        timeout: 10000,




        success: function (content) {
            console.log('Success ajax GET reload');
            $(".ajax-loader").replaceWith(content);
            $(".loading-icon").css("opacity", "0");
            if (content.indexOf('msg-table') !== -1) {
                if (content.indexOf('<p>') !== -1) {
                    var errTemplate = $('#hidden-template').html();
                    $('#msg-table').replaceWith(errTemplate);
                } else {
                    $('#msg-table').replaceWith('<div id="msg-table"></div>');
                }
            } else {
                if (content.indexOf('<p>') !== -1) {
                    var errTemplate = $('#hidden-template').html();
                    $('#msg').replaceWith(errTemplate);
                } else {
                    $('#msg').replaceWith('<div id="msg"></div>');
                }
            }
            $("#hidden-template").remove();
        }
    }).fail(function (jqXHR) {
        $(".loading-icon").css("opacity", "0");
        ajaxErrorHandler(jqXHR);
    });
}

function ajaxErrorHandler(jqXHR) {
    if (jqXHR.status === 500) {
        var errTemplate = ('<div class="alert alert-warning alert-dismissable" id="msg-table">' +
            '<button type="button" class="close" data-dismiss="alert" aria-hidden="true">×</button>' +
            '<span>An internal server error occurred. If the issue persists, contact system administrator.</span></div>');
    } else if (jqXHR.status === 404) {
        var errTemplate = ('<div class="alert alert-warning alert-dismissable" id="msg-table">' +
            '<button type="button" class="close" data-dismiss="alert" aria-hidden="true">×</button>' +
            '<span>It seems that you tried to access something that does not exist.</span></div>');
    } else {
        var errTemplate = ('<div class="alert alert-warning alert-dismissable" id="msg-table">' +
            '<button type="button" class="close" data-dismiss="alert" aria-hidden="true">×</button>' +
            '<span>An unexpected error occurred.</span></div>');
    }
    $('#msg-table').replaceWith(errTemplate);
}

