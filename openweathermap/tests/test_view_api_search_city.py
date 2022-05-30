from django.test import TestCase, override_settings
from openweathermap.utils import OpenWeatherMapUtil
from asynctest import CoroutineMock, patch
from django.core.cache import cache
from django.urls import reverse
import json


class TestUtilFindCityByName(TestCase):
    def setUp(self) -> None:
        self.EXPECTED_CITY_SUCCESS_RESPONSE = [
            {"id": "Bandung-ID", "name": "Bandung", "local_name": "Bandung", "lat": -6.9344694, "lon": 107.6049539,
             "country": "ID"},
            {"id": "Bandung-ID", "name": "Bandung", "local_name": "Bandung", "lat": -7.4419024, "lon": 112.3956465,
             "country": "ID"}, {"id": "Bandung-ID", "name": "Bandung", "local_name": "Bandung", "lat": -7.9066879,
                                "lon": 110.56400786469558, "country": "ID"},
            {"id": "Bandung-ID", "name": "Bandung", "local_name": "Bandung", "lat": -6.6777569, "lon": 110.804967,
             "country": "ID"},
            {"id": "Bandung-ID", "name": "Bandung", "local_name": "Bandung", "lat": -7.2986753, "lon": 110.6541023,
             "country": "ID"}]

    @override_settings(CACHES={
            'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache', 'LOCATION': 'weatherchallenge'}})
    def test_view_search_city_success(self):
        get_weather_url = f"{reverse('openweathermap:openweathermap_search_city_api')}?name=Bandung"
        response = self.client.get(path=get_weather_url)
        self.assertDictEqual(response.json(), {'cities': self.EXPECTED_CITY_SUCCESS_RESPONSE})

    @override_settings(CACHES={
        'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache', 'LOCATION': 'weatherchallenge'}})
    def test_view_search_city_success_in_cache(self):
        get_weather_url = f"{reverse('openweathermap:openweathermap_search_city_api')}?name=Bandung"
        response = self.client.get(path=get_weather_url)
        self.assertListEqual(cache.get('en_Bandung'), self.EXPECTED_CITY_SUCCESS_RESPONSE)

    @override_settings(CACHES={
        'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache', 'LOCATION': 'weatherchallenge'}})
    def test_view_search_city_failed_no_param_city(self):
        get_weather_url = f"{reverse('openweathermap:openweathermap_search_city_api')}"
        response = self.client.get(path=get_weather_url)
        self.assertEqual(response.status_code, 412)


