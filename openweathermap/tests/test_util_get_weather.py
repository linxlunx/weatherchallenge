from django.test import TestCase, override_settings
from openweathermap.utils import OpenWeatherMapUtil
from asynctest import CoroutineMock, patch
from django.core.cache import cache


class TestUtilGetWeather(TestCase):
    def setUp(self) -> None:
        self.LATITUDE = -6.9345
        self.LONGITUDE = 107.605

        self.MOCK_AIOHTTP_RESPONSE = {"coord": {"lon": 107.605, "lat": -6.9345}, "weather": [
            {"id": 803, "main": "Clouds", "description": "broken clouds", "icon": "04d"}], "base": "stations",
                                      "main": {"temp": 24.87, "feels_like": 25.45, "temp_min": 24.87, "temp_max": 24.87,
                                               "pressure": 1008, "humidity": 78, "sea_level": 1008, "grnd_level": 931},
                                      "visibility": 10000, "wind": {"speed": 2.01, "deg": 328, "gust": 2.9},
                                      "clouds": {"all": 75}, "dt": 1653901719,
                                      "sys": {"country": "ID", "sunrise": 1653864884, "sunset": 1653907184},
                                      "timezone": 25200, "id": 1650357, "name": "Bandung", "cod": 200}

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

    @override_settings(CACHES={'default': {'BACKEND': 'django.core.cache.backends.dummy.DummyCache'}})
    @patch('aiohttp.ClientSession.get')
    async def test_get_weather_success(self, mock_get):
        mock_get.return_value.__aenter__.return_value.json = CoroutineMock(side_effect=[
            self.MOCK_AIOHTTP_RESPONSE
        ])
        op = OpenWeatherMapUtil()
        response = await op.get_weather(self.LATITUDE, self.LONGITUDE)
        self.assertDictEqual(response['main'], self.EXPECTED_WEATHER_RESPONSE['main'])

    @override_settings(CACHES={
        'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache', 'LOCATION': 'weatherchallenge'}})
    @patch('aiohttp.ClientSession.get')
    async def test_get_weather_in_cache(self, mock_get):
        mock_get.return_value.__aenter__.return_value.json = CoroutineMock(side_effect=[
            self.MOCK_AIOHTTP_RESPONSE
        ])

        # check empty cache
        self.assertEqual(cache.get(f'en_{self.LATITUDE}_{self.LONGITUDE}'), None)

        op = OpenWeatherMapUtil()
        response = await op.get_weather(self.LATITUDE, self.LONGITUDE)

        # check data from cache
        self.assertDictEqual(cache.get(f'en_{self.LATITUDE}_{self.LONGITUDE}')['main'],
                             self.EXPECTED_WEATHER_RESPONSE['main'])
