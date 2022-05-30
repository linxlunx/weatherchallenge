FROM python:3.8

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY locale /src/locale
COPY manage.py /src/manage.py
COPY openweathermap /src/openweathermap
COPY static /src/static
COPY templates /src/templates
COPY weatherchallenge /src/weatherchallenge

WORKDIR /src

EXPOSE 80
CMD uvicorn weatherchallenge.asgi:application --host 0.0.0.0 --port 80
