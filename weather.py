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
        self.api_key = parser.get('wunderground.com', 'api_key')
        if len(self.api_key) == 0:
            print("You must enter your api key in the config.ini file. e.g. api_key:YOU_API_KEY")
            print("Exiting")
            sys.exit(1)
        client = MongoClient('localhost', 27017)
        self.db = client.weatherdb
        self.collection = self.db.weather_channel

    def get_current_temp(self):
        url = 'http://api.wunderground.com/api/{api_key}/conditions/q/CA/Palo_Alto.json'.format(api_key=self.api_key)
        response = urllib2.urlopen(url)
        json_string = response.read()
        parsed_json = json.loads(json_string)
        temp = parsed_json['current_observation']['temp_f']
        response.close()
        return temp

    def get_hourly(self):
        current_time = datetime.datetime.now()
        current_day = current_time.day
        url = 'http://api.wunderground.com/api/{api_key}/hourly/q/CA/Palo_Alto.json'.format(api_key=self.api_key)
        response = urllib2.urlopen(url)
        json_string = response.read()
        parsed_json = json.loads(json_string)
        hourly = parsed_json['hourly_forecast']
        response.close()
        data = []
        for i in range(len(hourly)):
            data_point = {}
            day = int(hourly[i]['FCTTIME']['mday'])
            data_point['temp'] = hourly[i]['temp']['english']
            data_point['humidity'] = hourly[i]['humidity']
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
                                             "humidity": float(data[i]['humidity']),
                                             "time": time,
                                             "month": date_tokens[4],
                                             "day": int(date_tokens[5].replace(',','')),
                                             "year": int(date_tokens[6])}},
                                   upsert=True)

if __name__ == "__main__":
    weather = Weather()
    print (weather.get_current_temp())
    weather.update_hourly_db()
    print "hourly updated"