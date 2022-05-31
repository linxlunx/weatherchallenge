# Weather Challenge

## Overview
Weather Challenge is a website to check the weather by location name. The website consumes weather data from [OpenWeatherMap](https://home.openweathermap.org). Register to [OpenWeatherMap](https://home.openweathermap.org) to get the api key.


## Prerequisites
- Python 3.8+
- Memcached

## Configuration
- Copy `.env.example` to `.env`
```
$ cp weatherchallenge/.env.example weatherchallenge/.env
``` 
- Fill `OPENWEATHERMAP_API_KEY` variable in `.env` with api key from [OpenWeatherMap](https://home.openweathermap.org)
- We are using [Memcached](https://memcached.org/) for the cache server. Set `MEMCACHED_HOST` for the memcached server.
- We can set the cache timeout (in minutes) by setting the `MEMCACHED_TIMEOUT`

## Run
- Install requirements
```
$ pip install -r requirements.txt
```
- Run with django server
```
$ python manage.py runserver
```
- Or run with uvicorn
```
$ uvicorn weatherchallenge.asgi:application
```
- Access the server on `http://127.0.0.1:8000`

## Docker
- Build docker image
```
$ docker build . -t weatherchallenge
```
- Run docker image with env file (map to port 8000)
```
$ docker run -it -p "8000:80" --env-file weatherchallenge/.env weatherchallenge
```
- Or you can build and run with docker-compose
```
$ docker-compose up --build
```

## Tests
- Create `test.env` file
```
$ cp weatherchallenge/.env.example weatherchallenge/test.env
```
- Fill `OPENWEATHERMAP_API_KEY` with real api key to do integration testing
- If the api key is not valid, only unit tests will be run
- Run test verbosely
```
$ python manage.py test -v 2
```