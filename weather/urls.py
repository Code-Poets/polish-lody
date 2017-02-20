from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$',                      views.WeatherIndex.as_view(),  			name='weather_index'),
    url(r'^forecast$',              views.WeatherForecast.as_view(),        name='weather_forecast'),
    url(r'^forecastdaily$',         views.WeatherForecastDaily.as_view(),   name='weather_forecastdaily'),
]