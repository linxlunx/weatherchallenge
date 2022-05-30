from django.test import TestCase
from openweathermap.utils import OpenWeatherMapUtil


class TestUtilConvertTemperature(TestCase):
    def test_convert_temperature_success(self):
        op = OpenWeatherMapUtil()
        self.assertListEqual(op.convert_temperature(10.02), [10.02, 50.04, 283.17])

    def test_convert_temperature_fail(self):
        op = OpenWeatherMapUtil()
        with self.assertRaises(ValueError) as err:
            op.convert_temperature('a')
