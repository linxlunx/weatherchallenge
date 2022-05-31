from django.test import TestCase
from openweathermap.utils import OpenWeatherMapUtil
from django.conf import settings


class TestUtilBuildURL(TestCase):
    def test_build_url_success_input_string(self):
        op = OpenWeatherMapUtil()
        path_url = 'test?'
        full_url = f'{op.API_URL}/test?&appid={settings.OPENWEATHERMAP_API_KEY}&lang=en'
        self.assertEqual(op.build_url(path_url), full_url)

    def test_build_url_success_input_integer(self):
        op = OpenWeatherMapUtil()
        path_url = 123
        full_url = f'{op.API_URL}/123&appid={settings.OPENWEATHERMAP_API_KEY}&lang=en'
        self.assertEqual(op.build_url(path_url), full_url)
