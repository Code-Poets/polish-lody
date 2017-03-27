from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class WeatherIndex(LoginRequiredMixin, TemplateView):
	template_name = "weather/weather_index.html"

class WeatherForecast(LoginRequiredMixin, TemplateView):
	template_name = "weather/weather_forecast.html"