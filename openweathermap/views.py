from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from . import forms
from . import utils


class OpenWeatherMapView(View):
    redirect_field_name = 'openweathermap'

    def get(self, request, *args, **kwargs):
        return render(request, 'openweathermap/index.html')

    def post(self, request, *args, **kwargs):
        form = forms.OpenWeatherMapGetDetailForm(request.POST)
        if not form.is_valid():
            return render(request, 'openweathermap/index.html', {'errors': form.errors})
        try:
            weather = utils.OpenWeatherMapUtil(request.LANGUAGE_CODE).get_weather(form.cleaned_data['latitude'],
                                                                                  form.cleaned_data['longitude'])
        except Exception as err:
            err_message = f'Error connect to openweathermap: {err}'
            return render(request, 'openweathermap/index.html', {'errors': err_message})
        return render(request, 'openweathermap/index.html', {'weather': weather, 'city': form.cleaned_data['city']})


class OpenWeatherMapAPIFindCityView(View):
    def get(self, request, *args, **kwargs):
        form = forms.OpenWeatherMapFindCityForm(request.GET)
        if not form.is_valid():
            return JsonResponse(status=412, data={'errors': form.errors})
        try:
            cities = utils.OpenWeatherMapUtil(request.LANGUAGE_CODE).find_city_by_name(form.cleaned_data['name'])
        except Exception as err:
            return JsonResponse(status=400, data={'errors': str(err)})
        return JsonResponse({'cities': cities})
