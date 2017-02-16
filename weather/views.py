from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

@login_required
def weather_index(request):
    return render(request, 'weather/weather_index.html', {})

@login_required
def weather_forecast(request):
    return render(request, 'weather/weather_forecast.html', {})

@login_required
def weather_forecastdaily(request):
    return render(request, 'weather/weather_forecastdaily.html', {})