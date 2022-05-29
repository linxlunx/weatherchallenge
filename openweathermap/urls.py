from django.urls import path

from . import views

app_name = 'openweathermap'
urlpatterns = [
    path('', views.OpenWeatherMapView.as_view(), name='index'),
    path('api/cities', views.OpenWeatherMapAPIFindCityView.as_view(), name='search_city_api')
]