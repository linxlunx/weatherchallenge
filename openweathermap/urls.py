from django.urls import path

from . import views

app_name = 'openweathermap'
urlpatterns = [
    path('', views.openweathermap_view, name='openweathermap_index'),
    path('api/cities', views.search_city, name='openweathermap_search_city_api')
]
