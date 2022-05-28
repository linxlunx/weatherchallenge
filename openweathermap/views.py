from django.shortcuts import render
from django.views import View


class OpenWeatherMapView(View):
    redirect_field_name = 'openweathermap'

    def get(self, request, *args, **kwargs):
        return render(request, 'openweathermap/index.html')
