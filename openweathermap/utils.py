from django.conf import settings
import aiohttp
from typing import List
from django.core.cache import cache
from decimal import Decimal
from . import decorators


class OpenWeatherMapUtil:
    def __init__(self, lang: str = None):
        self.API_URL = settings.OPENWEATHERMAP_API_URL
        self.API_KEY = settings.OPENWEATHERMAP_API_KEY
        if lang is None:
            lang = 'en'
        self.lang = lang
        self.directions = ['north', 'northeast', 'east', 'southeast', 'south', 'southwest', 'west', 'northwest']

    def build_url(self, path: str) -> str:
        url = f'{self.API_URL}/{path}&appid={self.API_KEY}&lang={self.lang}'
        return url

    async def get_url(self, url: str) -> dict:
        timeout = aiohttp.ClientTimeout(total=10)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            try:
                async with session.get(url) as response:
                    data = await response.json()
                    if 'cod' in data:
                        if data['cod'] != 200:
                            raise ValueError(data['message'])
                    return data
            except (aiohttp.ServerTimeoutError, aiohttp.ClientConnectorError) as err:
                raise ValueError(str(err))

    @decorators.use_cache
    async def find_city_by_name(self, city_name: str) -> List[dict]:
        """
        Get list of cities by names
        Return by local languanges if exist
        """
        location_search_path = f'geo/1.0/direct?q={city_name}&limit=5'
        location_search_url = self.build_url(location_search_path)
        resp = await self.get_url(location_search_url)
        cities = []
        for r in resp:
            # get local name if exist
            if 'local_names' in r:
                if self.lang in r['local_names']:
                    local_name = r['local_names'][self.lang]
                else:
                    local_name = r['name']
            else:
                local_name = r['name']

            if 'state' in r:
                state = r['state']
            else:
                state = local_name

            cities.append({
                'id': f"{r['name']}-{state}-{r['country']}",
                'name': r['name'],
                'local_name': local_name,
                'lat': r['lat'],
                'lon': r['lon'],
                'states': state,
                'country': r['country'],
            })

        # set cache
        cache.set(f'{self.lang}_{city_name}', cities)
        return cities

    @staticmethod
    def convert_temperature(temp_celcius: float) -> List[float]:
        """
        Convert temperature from Celcius to Fahrenheit and Kelvin
        """
        try:
            float(temp_celcius)
        except Exception as err:
            raise ValueError(err)

        temperatures = [temp_celcius, round(((temp_celcius * 9 / 5) + 32), 2), round((temp_celcius + 273.15), 2)]
        return temperatures

    @decorators.use_cache
    async def get_weather(self, lat: float, lon: float) -> dict:
        """
        Get weather detail from openweathermap
        """
        # get weather detail from openweathermap
        weather_detail_path = f'data/2.5/weather?lat={lat}&lon={lon}&units=metric'
        weather_detail_url = self.build_url(weather_detail_path)
        resp = await self.get_url(weather_detail_url)

        # convert degrees to direction
        degrees = (int(resp['wind']['deg'] * 8 / 360) + 8) % 8
        resp['direction'] = self.directions[degrees]

        # convert temperatures: C, F, K
        resp['temperatures'] = self.convert_temperature(resp['main']['temp'])
        resp['temperatures_min'] = self.convert_temperature(resp['main']['temp_min'])
        resp['temperatures_max'] = self.convert_temperature(resp['main']['temp_max'])

        resp['wind']['speed_mph'] = '{:.2f}'.format(resp['wind']['speed'] * 2.237)

        cache.set(f'{self.lang}_{lat}_{lon}', resp)
        return resp
