$(document).ready(function() {

    $('.datepicker').datepicker({
        dateFormat  : 'dd.mm.yy',
        changeMonth : true,
        changeYear  : true,
        showWeek    : true,
        showOtherMonths : true,
        showButtonPanel : true
    });

    $.datepicker.regional['pl'] = {
        closeText: "Zamknij",
        prevText: "&#x3C;Poprzedni",
        nextText: "Następny&#x3E;",
        currentText: "Dziś",
        monthNames: [ "Styczeń","Luty","Marzec","Kwiecień","Maj","Czerwiec",
        "Lipiec","Sierpień","Wrzesień","Październik","Listopad","Grudzień" ],
        monthNamesShort: [ "Sty","Lu","Mar","Kw","Maj","Cze",
        "Lip","Sie","Wrz","Pa","Lis","Gru" ],
        dayNames: [ "Niedziela","Poniedziałek","Wtorek","Środa","Czwartek","Piątek","Sobota" ],
        dayNamesShort: [ "Nie","Pn","Wt","Śr","Czw","Pt","So" ],
        dayNamesMin: [ "N","Pn","Wt","Śr","Cz","Pt","So" ],
        weekHeader: "Tydz",
        dateFormat: "dd.mm.yy",
        firstDay: 1,
        isRTL: false,
        showMonthAfterYear: false,
        yearSuffix: "" };
    $.datepicker.setDefaults($.datepicker.regional['pl']);

});

$(document).ready(function(){

    var weather_apixu = "https://api.apixu.com/v1/forecast.json?key=e3acfecab7234cd4b26110712172102&q=Wroclaw&days=7";
    $.getJSON(weather_apixu, function(data){
        var weatherType = data.current.condition.text;
        var windSpeed = (data.current.wind_kph).toFixed(0);
        var cTemp = Math.round(data.current.temp_c);
        var feelslikeTemp = Math.round(data.current.feelslike_c);
        var pressure = (data.current.pressure_mb).toFixed(0);
        var humidity = data.current.humidity;
        var clouds = data.current.cloud;
        var icon = data.current.condition.icon;
        var iconSrc = "http:" + icon;

        $("#weatherType").html(weatherType);
        $("#windSpeed").html("wind: " + windSpeed + " km/h");
        $("#cTemp1").html("temp: " + cTemp.toFixed(0) + " &#8451");
        $("#cTemp2").html(cTemp.toFixed(0) + " &#8451");
        $("#feelslikeTemp").html("feels like: " + feelslikeTemp.toFixed(0) + " &#8451");
        $("#pressure").html("pressure: "+ pressure + " hPa");
        $("#humidity").html("humidity: "+ humidity + " %");
        $("#clouds").html("cloudiness: "+ clouds + " %");
        $("#weather").prepend('<img src="'+ iconSrc+ '">');
    }); //get JSON api function

    $('#weather').popover({
        html : true,
        content: function() {
          var content = $(this).attr("data-popover-content");
          return $(content).children(".popover-body").html();
        },
        title: function() {
          var title = $(this).attr("data-popover-content");
          return $(title).children(".popover-heading").html();
        }
    })
    .on("mouseenter", function () {
        var _this = this;
        $(this).popover("show");
        $(".popover").on("mouseleave", function () {
            $(_this).popover('hide');
        });
    }).on("mouseleave", function () {
        var _this = this;
        setTimeout(function () {
            if (!$(".popover:hover").length) {
                $(_this).popover("hide");
            }
        }, 300);
    });
});
