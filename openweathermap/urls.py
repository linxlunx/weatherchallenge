from django.urls import path

from . import views

app_name = 'openweathermap'
urlpatterns = [
    path('', views.OpenWeatherMapView.as_view(), name='index')
]
