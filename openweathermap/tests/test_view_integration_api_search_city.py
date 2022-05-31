from django.test import TestCase, override_settings
from django.urls import reverse
from django.core.cache import cache
from http.cookies import SimpleCookie
from unittest import skipIf
from openweathermap.tests.test_integration_helper import validate_openweathermap_key


@skipIf(not validate_openweathermap_key(), 'Please set valid API key')
class TestViewIntegrationAPISearchCity(TestCase):
    def setUp(self) -> None:
        self.name = 'Berlin'

    @override_settings(CACHES={
        'default': {'BACKEND': 'django.core.cache.backends.dummy.DummyCache'}})
    def test_view_integration_api_search_city(self):
        get_city_url = f"{reverse('openweathermap:openweathermap_search_city_api')}?name={self.name}"
        response = self.client.get(get_city_url)
        result = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertIn('cities', result)
        self.assertGreater(len(result['cities']), 0)

    @override_settings(CACHES={
        'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'}})
    def test_view_integration_api_search_city_with_cache(self):
        get_city_url = f"{reverse('openweathermap:openweathermap_search_city_api')}?name={self.name}"
        response = self.client.get(get_city_url)
        self.assertEqual(response.status_code, 200)
        cached = cache.get(f'en_{self.name}')
        self.assertNotEqual(cached, None)
        self.assertEqual(type(cached), list)

    @override_settings(CACHES={
        'default': {'BACKEND': 'django.core.cache.backends.dummy.DummyCache'}})
    def test_view_integration_api_search_city_no_param(self):
        get_city_url = f"{reverse('openweathermap:openweathermap_search_city_api')}"
        response = self.client.get(get_city_url)
        self.assertEqual(response.status_code, 412)

    @override_settings(CACHES={
        'default': {'BACKEND': 'django.core.cache.backends.dummy.DummyCache'}})
    def test_view_integration_api_search_city_get_response_italy(self):
        get_city_url = f"{reverse('openweathermap:openweathermap_search_city_api')}?name={self.name}"
        self.client.cookies = SimpleCookie({'django_language': 'it'})
        response = self.client.get(get_city_url)
        self.client.cookies = SimpleCookie({})
        result = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertIn('cities', result)
        self.assertGreater(len(result['cities']), 0)
        self.assertEqual(result['cities'][0]['local_name'], 'Berlino')


