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
    if (localStorage.getItem('lscache-navbarWeatherData')==null) {
        $.getJSON(weather_apixu, function(data) {
            lscache.set('navbarWeatherData', data, 60);
            var localWeatherData = JSON.parse(localStorage.getItem('lscache-navbarWeatherData'));
            NavbarWeatherData();
        });
    } else {
        NavbarWeatherData();
    }

    function NavbarWeatherData(){
        var localData = JSON.parse(localStorage.getItem('lscache-navbarWeatherData'));
        if(template_lang == "pl"){
            function readTextFile(file, callback) {
                var rawFile = new XMLHttpRequest();
                rawFile.overrideMimeType("application/json");
                rawFile.open("GET", file, true);
                rawFile.onreadystatechange = function() {
                    if (rawFile.readyState === 4 && rawFile.status == "200") {
                        callback(rawFile.responseText);
                    }
                }
                rawFile.send(null);
            }
            readTextFile("../../static/js/conditions.json", function(text){
                var data = JSON.parse(text);
                if(sessionStorage.getItem('conditions_trans')==null){
                    sessionStorage.setItem('conditions_trans',JSON.stringify(data));
                }
                $.each(data, function(key, val){
                    if(val.code == localData.current.condition.code){
                        weatherType = val.languages[19].day_text
                        $("#weatherType").html(weatherType);
                    }
                });
            });
        } else {
            var weatherType = localData.current.condition.text;
            $("#weatherType").html(weatherType);
        }
        var windSpeed = (localData.current.wind_kph).toFixed(0);
        var cTemp = Math.round(localData.current.temp_c);
        var feelslikeTemp = Math.round(localData.current.feelslike_c);
        var pressure = (localData.current.pressure_mb).toFixed(0);
        var humidity = localData.current.humidity;
        var clouds = localData.current.cloud;
        var icon = localData.current.condition.icon;
        var iconSrc = "https:" + icon;

        $("#windSpeed").html(windSpeed + " km/h");
        $("#cTemp1").html(cTemp.toFixed(0) + " &#8451");
        $("#cTemp2").html(cTemp.toFixed(0) + " &#8451");
        $("#feelslikeTemp").html(feelslikeTemp.toFixed(0) + " &#8451");
        $("#pressure").html(pressure + " hPa");
        $("#humidity").html(humidity + " %");
        $("#clouds").html(clouds + " %");
        $("#weather").prepend('<img src="'+ iconSrc+ '">');
    }

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
