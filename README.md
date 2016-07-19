# Weather Service

A service to read hourly weather predictions from wunderground.com and store the temperature, temperature feel, humidity, conditions (cloud cover), and conditions url (icon graphic of cloud cover) to mongodb.


## Prerequisites
You need to have the following installed:

- [MongoDB](http://www.mongodb.org) and must be running
- [pymongo](https://docs.mongodb.com/getting-started/python/client/)
- [wunderground API Key](https://www.wunderground.com/weather/api/)

## Install

Note: make sure mongdb is running whenever using this service


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

