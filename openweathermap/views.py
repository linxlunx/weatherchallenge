from django.shortcuts import render
from django.http import JsonResponse
from . import forms
from . import utils


async def openweathermap_view(request):
    if request.method == 'GET':
        return render(request, 'openweathermap/index.html')
    if request.method == 'POST':
        form = forms.OpenWeatherMapGetDetailForm(request.POST)
        if not form.is_valid():
            return render(request, 'openweathermap/index.html', {'errors': form.errors})
        try:
            weather = await utils.OpenWeatherMapUtil(request.LANGUAGE_CODE).get_weather(form.cleaned_data['latitude'],
                                                                                        form.cleaned_data['longitude'])
        except Exception as err:
            err_message = f'Error connect to openweathermap: {err}'
            return render(request, 'openweathermap/index.html', {'errors': err_message})
        return render(request, 'openweathermap/index.html', {'weather': weather, 'city': form.cleaned_data['city']})


async def search_city(request):
    form = forms.OpenWeatherMapFindCityForm(request.GET)
    if not form.is_valid():
        return JsonResponse(status=412, data={'errors': form.errors})
    try:
        cities = await utils.OpenWeatherMapUtil(request.LANGUAGE_CODE).find_city_by_name(form.cleaned_data['name'])
    except Exception as err:
        return JsonResponse(status=400, data={'errors': str(err)})
    return JsonResponse({'cities': cities})
