# Weather Service

A service to read hourly weather predictions from wunderground.com and store the temperature, temperature feel, humidity, conditions (cloud cover), and conditions url (icon graphic of cloud cover) to mongodb.


## Prerequisites
You need to have the following installed:

- [MongoDB](http://www.mongodb.org) and must be running
- [pymongo](https://docs.mongodb.com/getting-started/python/client/)

And you need an [wunderground API Key](https://www.wunderground.com/weather/api/)


## Install

Install and run via Docker ([Weather Service Docker Repository](https://hub.docker.com/r/cpitzak/weather-service/)):
```
$ docker pull cpitzak/weather-service:1.0.0
$ docker run -e "WEATHER_SERVICE_MONGO_URL=mongodb://your_monog_url/weatherdb" \
             -e "WEATHER_SERVICE_API_KEY=wunderground.com_api_key" \
		     -e "WEATHER_SERVICE_HOURLY_URL=http://api.wunderground.com/api/your_api_key/hourly/q/CA/Palo_Alto.json" \
			 -e "WEATHER_SERVICE_HOURLY_STATE=CA" \
			 -e "WEATHER_SERVICE_HOURLY_CITY=Palo Alto" \
			 -e "WEATHER_SERVICE_DELAY=15" \
             cpitzak/weather-service:1.0.0
```

Or Build a docker image and run
```
$ docker build -t cpitzak/weather-service .
$ docker run -e "WEATHER_SERVICE_MONGO_URL=mongodb://your_monog_url/weatherdb" \
             -e "WEATHER_SERVICE_API_KEY=wunderground.com_api_key" \
		     -e "WEATHER_SERVICE_HOURLY_URL=http://api.wunderground.com/api/your_api_key/hourly/q/CA/Palo_Alto.json" \
			 -e "WEATHER_SERVICE_HOURLY_STATE=CA" \
			 -e "WEATHER_SERVICE_HOURLY_CITY=Palo Alto" \
			 -e "WEATHER_SERVICE_DELAY=15" \
             cpitzak/weather-service
```

Or to setup Manually
```
$ sudo mkdir /apps
$ sudo chown pi /apps
$ cd /apps
$ git clone https://github.com/cpitzak/weatherService.git
$ cd weatherService
$ [edit config.ini with your wunderground API key, hourly url for your city/state, and your city/state]
$ crontab -e
   add the following line: */15 * * * * /usr/bin/python /apps/weatherService/weather.py
$ sudo shutdown -r now
```
This service is a dependency to my other project [weatherWeb](https://github.com/cpitzak/weatherWeb).

