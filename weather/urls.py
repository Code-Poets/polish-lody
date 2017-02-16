from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$',                      views.weather_index,           name='weather_index'),
    url(r'^forecast$',              views.weather_forecast,        name='weather_forecast'),
    url(r'^forecastdaily$',         views.weather_forecastdaily,   name='weather_forecastdaily'),
]