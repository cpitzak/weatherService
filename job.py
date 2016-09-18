import os
import time
from ConfigParser import SafeConfigParser
from weather import Weather

weather = Weather()
parser = SafeConfigParser()
cwd = os.path.dirname(os.path.realpath(__file__))
parser.read(os.path.join(cwd, 'config.ini'))
delay = float(os.getenv('WEATHER_SERVICE_DELAY', parser.get('wunderground.com', 'delay')))

while True:
	weather.update_hourly_db()
	time.sleep(60 * delay)