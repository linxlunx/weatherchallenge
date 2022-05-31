from django.conf import settings
from urllib import request, error


def validate_openweathermap_key() -> bool:
    api_url = f'{settings.OPENWEATHERMAP_API_URL}/geo/1.0/direct?q=Berlin&limit=5&appid={settings.OPENWEATHERMAP_API_KEY}'
    try:
        request.urlopen(api_url)
    except error.HTTPError as e:
        return False
    return True


