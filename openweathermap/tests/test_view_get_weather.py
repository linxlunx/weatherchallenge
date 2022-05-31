from django.test import TestCase, override_settings
from asynctest import patch
from django.urls import reverse


class TestViewGetWeather(TestCase):
    def setUp(self) -> None:
        self.LATITUDE = -6.9345
        self.LONGITUDE = 107.605
        self.city = 'Bandung-ID'
        self.EXPECTED_WEATHER_RESPONSE = {'coord': {'lon': 107.605, 'lat': -6.9345}, 'weather': [
            {'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04d'}], 'base': 'stations',
                                          'main': {'temp': 24.87, 'feels_like': 25.45, 'temp_min': 24.87,
                                                   'temp_max': 24.87, 'pressure': 1008, 'humidity': 78,
                                                   'sea_level': 1008, 'grnd_level': 931}, 'visibility': 10000,
                                          'wind': {'speed': 2.01, 'deg': 328, 'gust': 2.9}, 'clouds': {'all': 75},
                                          'dt': 1653901785,
                                          'sys': {'country': 'ID', 'sunrise': 1653864884, 'sunset': 1653907184},
                                          'timezone': 25200, 'id': 1650357, 'name': 'Bandung', 'cod': 200,
                                          'direction': 'northwest', 'temperatures': [24.87, 76.77, 298.02],
                                          'temperatures_min': [24.87, 76.77, 298.02],
                                          'temperatures_max': [24.87, 76.77, 298.02]}

    @override_settings(CACHES={
        'default': {'BACKEND': 'django.core.cache.backends.dummy.DummyCache'}})
    @patch('openweathermap.utils.OpenWeatherMapUtil.get_weather')
    def test_view_get_weather_success(self, mock_value):
        mock_value.return_value = self.EXPECTED_WEATHER_RESPONSE
        get_weather_url = f"{reverse('openweathermap:openweathermap_index')}"
        response = self.client.post(path=get_weather_url,
                                    data={'city': self.city, 'latitude': self.LATITUDE, 'longitude': self.LONGITUDE})
        result = response.content.decode('utf-8')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Temperature', result)
        self.assertIn('24.87', result)
        self.assertIn('northwest', result)

    @override_settings(CACHES={
        'default': {'BACKEND': 'django.core.cache.backends.dummy.DummyCache'}})
    def test_view_get_weather_failed_no_param(self):
        get_city_url = f"{reverse('openweathermap:openweathermap_index')}"
        response = self.client.post(path=get_city_url, data={})
        self.assertIn("Please Check City Name", response.content.decode('utf-8'))

    @override_settings(CACHES={
        'default': {'BACKEND': 'django.core.cache.backends.dummy.DummyCache'}})
    def test_view_get_weather_failed_wrong_param(self):
        get_weather_url = f"{reverse('openweathermap:openweathermap_index')}"
        response = self.client.post(path=get_weather_url,
                                    data={"name": "Bandung-ID", "longitude": "abc", "latitude": "def"})
        self.assertIn("Please Check City Name", response.content.decode('utf-8'))
