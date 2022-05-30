from django.test import TestCase
from openweathermap.utils import OpenWeatherMapUtil
from asynctest import CoroutineMock, patch


class TestUtilGetURL(TestCase):
    @patch('aiohttp.ClientSession.get')
    async def test_get_url_success_with_mock(self, mock_get):
        mock_get.return_value.__aenter__.return_value.json = CoroutineMock(side_effect=[
            {'cod': 200, 'message': 'success'}
        ])
        op = OpenWeatherMapUtil()
        response = await op.get_url('https://google.com')
        self.assertDictEqual(response, {'cod': 200, 'message': 'success'})

    @patch('aiohttp.ClientSession.get')
    async def test_get_url_invalid_code_with_mock(self, mock_get):
        mock_get.return_value.__aenter__.return_value.json = CoroutineMock(side_effect=[
            {'cod': 400, 'message': 'success'}
        ])
        op = OpenWeatherMapUtil()
        with self.assertRaises(ValueError) as err:
            resp = await op.get_url('https://google.com')

    async def test_get_url_invalid_link(self):
        op = OpenWeatherMapUtil()
        with self.assertRaises(ValueError) as err:
            resp = await op.get_url('http://invalid.link')
