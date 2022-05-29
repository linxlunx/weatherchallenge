from django import forms


class OpenWeatherMapFindCityForm(forms.Form):
    name = forms.CharField(min_length=3)


class OpenWeatherMapGetDetailForm(forms.Form):
    city = forms.CharField()
    latitude = forms.FloatField()
    longitude = forms.FloatField()

