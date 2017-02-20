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

    var api = "http://api.openweathermap.org/data/2.5/weather?id=3081368&units=metric&appid=dfab07a2d2cea2d6179fd5f8770a90cb";
    $.getJSON(api, function(data){
        var weatherType = data.weather[0].description;
        var windSpeed = ((data.wind.speed)*3.6).toFixed(0);
        var cTemp = Math.round(data.main.temp);
        var pressure = (data.main.pressure).toFixed(0);
        var humidity = data.main.humidity;
        var clouds = data.clouds.all;
        var icon = data.weather[0].icon;
        var iconSrc = "http://openweathermap.org/img/w/" + icon + ".png";

        $("#weatherType").html(weatherType);
        $("#windSpeed").html("wind: " + windSpeed + " km/h");
        $("#cTemp1").html("temp: " + cTemp.toFixed(0) + " &#8451");
        $("#cTemp2").html(cTemp.toFixed(0) + " &#8451");
        $("#pressure").html("pressure: "+ pressure + " hPa")
        $("#humidity").html("humidity: "+ humidity + " %")
        $("#clouds").html("cloudiness: "+ clouds + " %")
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
