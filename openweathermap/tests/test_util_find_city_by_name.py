from django.test import TestCase, override_settings
from openweathermap.utils import OpenWeatherMapUtil
from asynctest import CoroutineMock, patch
from django.core.cache import cache


class TestUtilFindCityByName(TestCase):
    def setUp(self) -> None:
        self.MOCK_AIOHTTP_RESPONSE = [{'name': 'Bandung',
                                       'local_names': {'ja': 'バンドン', 'oc': 'Bandung', 'uk': 'Бандунг', 'zh': '万隆',
                                                       'nl': 'Bandoeng', 'kn': 'ಬಾಂದುಂಗ್', 'ru': 'Бандунг',
                                                       'en': 'Bandung', 'id': 'Bandung'}, 'lat': -6.9344694,
                                       'lon': 107.6049539, 'country': 'ID', 'state': 'West Java'},
                                      {'name': 'Bandung', 'lat': -7.4419024, 'lon': 112.3956465, 'country': 'ID',
                                       'state': 'East Java'},
                                      {'name': 'Bandung', 'lat': -7.9066879, 'lon': 110.56400786469558, 'country': 'ID',
                                       'state': 'Special Region of Yogyakarta'},
                                      {'name': 'Bandung', 'lat': -6.6777569, 'lon': 110.804967, 'country': 'ID',
                                       'state': 'Central Java'},
                                      {'name': 'Bandung', 'lat': -7.2986753, 'lon': 110.6541023, 'country': 'ID',
                                       'state': 'Central Java'}]
        self.EXPECTED_CITY_SUCCESS_RESPONSE = [
            {"id": "Bandung-West Java-ID", "name": "Bandung", "local_name": "Bandung", "lat": -6.9344694,
             "lon": 107.6049539, "states": "West Java", "country": "ID"},
            {"id": "Bandung-East Java-ID", "name": "Bandung", "local_name": "Bandung", "lat": -7.4419024,
             "lon": 112.3956465, "states": "East Java", "country": "ID"},
            {"id": "Bandung-Special Region of Yogyakarta-ID", "name": "Bandung", "local_name": "Bandung",
             "lat": -7.9066879, "lon": 110.56400786469558, "states": "Special Region of Yogyakarta", "country": "ID"},
            {"id": "Bandung-Central Java-ID", "name": "Bandung", "local_name": "Bandung", "lat": -6.6777569,
             "lon": 110.804967, "states": "Central Java", "country": "ID"},
            {"id": "Bandung-Central Java-ID", "name": "Bandung", "local_name": "Bandung", "lat": -7.2986753,
             "lon": 110.6541023, "states": "Central Java", "country": "ID"}]

    @override_settings(CACHES={'default': {'BACKEND': 'django.core.cache.backends.dummy.DummyCache'}})
    @patch('aiohttp.ClientSession.get')
    async def test_find_city_by_name_success(self, mock_get):
        mock_get.return_value.__aenter__.return_value.json = CoroutineMock(side_effect=[
            self.MOCK_AIOHTTP_RESPONSE
        ])
        op = OpenWeatherMapUtil()
        response = await op.find_city_by_name('Bandung')
        self.assertListEqual(response, self.EXPECTED_CITY_SUCCESS_RESPONSE)

    @override_settings(CACHES={
        'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache', 'LOCATION': 'weatherchallenge'}})
    @patch('aiohttp.ClientSession.get')
    async def test_find_city_by_name_check_value_in_cache(self, mock_get):
        mock_get.return_value.__aenter__.return_value.json = CoroutineMock(side_effect=[
            self.MOCK_AIOHTTP_RESPONSE
        ])

        # check empty cache
        self.assertEqual(cache.get('en_Bandung'), None)

        op = OpenWeatherMapUtil()
        response = await op.find_city_by_name('Bandung')

        # check data from cache
        self.assertListEqual(cache.get('en_Bandung'), self.EXPECTED_CITY_SUCCESS_RESPONSE)
