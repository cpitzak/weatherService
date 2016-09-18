#https://www.wunderground.com/weather/api
import datetime
import json
import os
import sys
import urllib2
from ConfigParser import SafeConfigParser
from pymongo import MongoClient


class Weather:

    def __init__(self):
        parser = SafeConfigParser()
        cwd = os.path.dirname(os.path.realpath(__file__))
        parser.read(os.path.join(cwd, 'config.ini'))
        self.api_key = os.getenv('WEATHER_SERVICE_API_KEY', parser.get('wunderground.com', 'api_key'))
        self.hourly_url = os.getenv('WEATHER_SERVICE_HOURLY_URL', parser.get('wunderground.com', 'hourly_url'))
        self.hourly_state = os.getenv('WEATHER_SERVICE_HOURLY_STATE', parser.get('wunderground.com', 'hourly_state'))
        self.hourly_city = os.getenv('WEATHER_SERVICE_HOURLY_CITY', parser.get('wunderground.com', 'hourly_city'))
        self.mongodb_url = os.getenv('WEATHER_SERVICE_MONGO_URL', parser.get('urls', 'mongodb'))
        self.validate_config()
        client = MongoClient(self.mongodb_url)
        self.db = client.weatherdb
        self.collection = self.db.weather_channel
        self.meta_data = self.db.meta_data
        self.meta_data.update({"location": { "$exists": True }},
                               {"$set": {"location.state": self.hourly_state, "location.city": self.hourly_city}},
                               upsert=True)

    def validate_config(self):
        if len(self.api_key) == 0:
            print("You must enter your api key in the config.ini file. e.g. api_key:YOU_API_KEY")
            print("Exiting")
            sys.exit(1)
        if len(self.hourly_url) == 0:
            print("You must enter the weatherunderground.com hourly url in the config.ini file. "
                "e.g. hourly_url: http://api.wunderground.com/api/%(api_key)s/hourly/q/CA/Palo_Alto.json")
            print("Exiting")
            sys.exit(1)
        if len(self.hourly_state) == 0:
            print("You must enter the state in the config.ini file. e.g. hourly_state: CA")
            print("Exiting")
            sys.exit(1)
        if len(self.hourly_city) == 0:
            print("You must enter the city in the config.ini file. e.g. hourly_city: Palo Alto")
            print("Exiting")
            sys.exit(1)
        if len(self.mongodb_url) == 0:
            print("You must specify the mongodb url in config.ini file.")
            sys.exit(1)

    def get_hourly(self):
        current_time = datetime.datetime.now()
        current_day = current_time.day
        response = urllib2.urlopen(self.hourly_url)
        json_string = response.read()
        parsed_json = json.loads(json_string)
        hourly = parsed_json['hourly_forecast']
        response.close()
        data = []
        for i in range(len(hourly)):
            data_point = {}
            day = int(hourly[i]['FCTTIME']['mday'])
            data_point['temp'] = hourly[i]['temp']['english']
            data_point['temp_feel'] = hourly[i]['feelslike']['english']
            data_point['humidity'] = hourly[i]['humidity']
            data_point['condition'] = hourly[i]['condition']
            data_point['condition_icon_url'] = hourly[i]['icon_url']
            data_point['date'] = hourly[i]['FCTTIME']['pretty']
            data.append(data_point)
            # checking at end to get 12:00 AM
            if day > current_day:
                break
        return data

    def update_hourly_db(self):
        data = self.get_hourly()
        for i in range(len(data)):
            date_tokens = data[i]['date'].split(' ')
            # 12:00 AM PDT on June 29, 2016
            # ["12:00", "AM", "PDT", "on", "June", "29,", "2016"]
            time = "{0} {1}".format(date_tokens[0], date_tokens[1])
            self.collection.update({'date': data[i]['date']},
                                   {"$set": {"temp": float(data[i]['temp']),
                                             "temp_feel": float(data[i]['temp_feel']),
                                             "humidity": float(data[i]['humidity']),
                                             "condition": data[i]['condition'],
                                             "condition_icon_url": data[i]['condition_icon_url'],
                                             "time": time,
                                             "month": date_tokens[4],
                                             "day": int(date_tokens[5].replace(',','')),
                                             "year": int(date_tokens[6])}},
                                   upsert=True)

if __name__ == "__main__":
    weather = Weather()
    weather.update_hourly_db()
