from django.test import TestCase, override_settings
from django.urls import reverse
import re
from django.core.cache import cache
from http.cookies import SimpleCookie


class TestViewIntegrationGetWeather(TestCase):
    def setUp(self) -> None:
        self.LATITUDE = -6.9345
        self.LONGITUDE = 107.605

    @override_settings(CACHES={
        'default': {'BACKEND': 'django.core.cache.backends.dummy.DummyCache'}})
    def test_view_integration_get_weather_success(self):
        get_weather_url = f"{reverse('openweathermap:openweathermap_index')}"
        response = self.client.post(path=get_weather_url,
                                    data={'city': 'Bandung-ID', 'latitude': self.LATITUDE, 'longitude': self.LONGITUDE})
        result = response.content.decode('utf-8')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Temperature', result)
        self.assertIn('Minimum Temperature', result)
        self.assertIn('Maximum Temperature', result)

    @override_settings(CACHES={
        'default': {'BACKEND': 'django.core.cache.backends.dummy.DummyCache'}})
    @override_settings(OPENWEATHERMAP_API_URL='https://google.com')
    def test_view_integration_get_wrong_url(self):
        get_weather_url = f"{reverse('openweathermap:openweathermap_index')}"
        response = self.client.post(path=get_weather_url,
                                    data={'city': 'Bandung-ID', 'latitude': self.LATITUDE, 'longitude': self.LONGITUDE})
        result = response.content.decode('utf-8')
        self.assertIn('Please Check', result)

    @override_settings(CACHES={
        'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'}})
    def test_view_integration_get_from_cache(self):
        get_weather_url = f"{reverse('openweathermap:openweathermap_index')}"
        response = self.client.post(path=get_weather_url,
                                    data={'city': 'Bandung-ID', 'latitude': self.LATITUDE, 'longitude': self.LONGITUDE})
        result = response.content.decode('utf-8')
        temp_result = re.findall(r'<td>(.*) \&\#8451\;</td>', result)

        cached = cache.get(f'en_{self.LATITUDE}_{self.LONGITUDE}')
        self.assertListEqual(temp_result,
                             [str(cached['temperatures'][0]), str(cached['temperatures_min'][0]),
                              str(cached['temperatures_max'][0])])

    @override_settings(CACHES={
        'default': {'BACKEND': 'django.core.cache.backends.dummy.DummyCache'}})
    def test_view_integration_get_weather_success_in_france(self):
        get_weather_url = f"{reverse('openweathermap:openweathermap_index')}"

        # set cookie to france
        self.client.cookies = SimpleCookie({'django_language': 'fr'})
        response = self.client.post(path=get_weather_url,
                                    data={'city': 'Bandung-ID', 'latitude': self.LATITUDE, 'longitude': self.LONGITUDE})
        result = response.content.decode('utf-8')
        # unset cookie
        self.client.cookies = SimpleCookie({})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Température', result)
        self.assertIn('Température minimale', result)
        self.assertIn('Température maximale', result)

    @override_settings(CACHES={
        'default': {'BACKEND': 'django.core.cache.backends.dummy.DummyCache'}})
    def test_view_integration_get_weather_no_param_in_france(self):
        get_weather_url = f"{reverse('openweathermap:openweathermap_index')}"

        # set cookie to france
        self.client.cookies = SimpleCookie({'django_language': 'fr'})
        response = self.client.post(path=get_weather_url, data={})
        result = response.content.decode('utf-8')
        # unset cookie
        self.client.cookies = SimpleCookie({})
        self.assertIn('Veuillez vérifier le nom de la ville', result)

    @override_settings(CACHES={
        'default': {'BACKEND': 'django.core.cache.backends.dummy.DummyCache'}})
    def test_view_integration_get_weather_success_in_italy(self):
        get_weather_url = f"{reverse('openweathermap:openweathermap_index')}"

        # set cookie to italy
        self.client.cookies = SimpleCookie({'django_language': 'it'})
        response = self.client.post(path=get_weather_url,
                                    data={'city': 'Bandung-ID', 'latitude': self.LATITUDE, 'longitude': self.LONGITUDE})
        result = response.content.decode('utf-8')
        # unset cookie
        self.client.cookies = SimpleCookie({})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Temperatura', result)
        self.assertIn('Temperatura minima', result)
        self.assertIn('Temperatura massima', result)

    @override_settings(CACHES={
        'default': {'BACKEND': 'django.core.cache.backends.dummy.DummyCache'}})
    def test_view_integration_get_weather_no_param_in_italy(self):
        get_weather_url = f"{reverse('openweathermap:openweathermap_index')}"

        # set cookie to italy
        self.client.cookies = SimpleCookie({'django_language': 'it'})
        response = self.client.post(path=get_weather_url, data={})
        result = response.content.decode('utf-8')
        # unset cookie
        self.client.cookies = SimpleCookie({})
        self.assertIn('Si prega di controllare il nome della città', result)

