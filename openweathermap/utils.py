from django.conf import settings
import aiohttp
import asyncio
from typing import List
from django.core.cache import cache
from decimal import Decimal
from datetime import datetime


class OpenWeatherMapUtil:
    def __init__(self, lang: str = None):
        self.API_URL = settings.OPENWEATHERMAP_API_URL
        self.API_KEY = settings.OPENWEATHERMAP_API_KEY
        if lang is None:
            lang = 'en'
        self.lang = lang

    async def get_url(self, path: str) -> dict:
        async with aiohttp.ClientSession() as session:
            try:
                url = f'{self.API_URL}/{path}&appid={self.API_KEY}&lang={self.lang}'
                async with session.get(url) as response:
                    data = await response.json()
                    return data
            except (aiohttp.ServerTimeoutError, aiohttp.ClientConnectorError) as err:
                print(err)

    def find_city_by_name(self, city_name: str) -> List[dict]:
        # check query in cache
        cache_key = f'city_{self.lang}_{city_name}'
        city_exist = cache.get(cache_key)
        if city_exist:
            return city_exist

        # get cities list from openweathermap
        location_search_url = f'geo/1.0/direct?q={city_name}&limit=5'
        resp = asyncio.run(self.get_url(location_search_url))
        cities = []
        for i, r in enumerate(resp):
            if 'local_names' in r:
                if self.lang in r['local_names']:
                    local_name = r['local_names'][self.lang]
                else:
                    local_name = r['name']
            else:
                local_name = r['name']

            cities.append({
                'id': f"{r['name']}-{r['country']}",
                'name': r['name'],
                'local_name': local_name,
                'lat': r['lat'],
                'lon': r['lon'],
                'country': r['country'],
            })

        # set cache
        cache.set(cache_key, cities)
        return cities

    def get_weather(self, lat: Decimal, lon: Decimal) -> dict:
        # check weather by lat lon in cache
        cache_key = f'weather_{self.lang}_{lat}_{lon}'
        weather_exist = cache.get(cache_key)
        if weather_exist:
            return weather_exist

        # get weather detail from openweathermap
        weather_detail_url = f'data/2.5/weather?lat={lat}&lon={lon}&units=metric'
        resp = asyncio.run(self.get_url(weather_detail_url))
        cache.set(cache_key, resp)
        return resp
