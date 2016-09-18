#!/usr/bin/env python3
import urllib.request, urllib.parse
from xml.dom import minidom
import json
import datetime
import codecs
import argparse

parser = argparse.ArgumentParser(description="Weather data")
parser.add_argument("--template", type=argparse.FileType('r', encoding='utf-8'), help="Teamplate file to parse")
parser.add_argument("--output", type=argparse.FileType('a', encoding='utf-8'), help="Output file to write")

args = parser.parse_args()

# Code of my city, if you don't know what to do here, read the README
CODE = "39292"
# Units should be 'c' or 'f'
UNITS='c'

baseurl = "https://query.yahooapis.com/v1/public/yql?"
yql_query = urllib.parse.quote("select * from weather.forecast where u='" + UNITS + "' and woeid=" + CODE)
yql_url = baseurl + "q=" + yql_query +"&format=json"

print(yql_url)

weather = urllib.request.urlopen(yql_url)

data = json.loads(codecs.decode(weather.read(), "utf-8"))
print(data)
forecast = data['query']['results']['channel']['item']['forecast']
print(forecast)

# Open SVG to process
output = args.template.read()

print("Forecast:")
print(forecast)

days = { "Mon": "Monday", "Tue": "Tuesday", "Wed": "Wednesday", "Thu": "Thursday", "Fri": "Friday", "Sat": "Saturday", "Sun": "Sunday" }

for i in range(len(forecast)):
	day = forecast[i]

	day["day"] = days[day["day"]]
	print("Day:")
	print(day)

	image_url = 'icons/' + day['code'] + '.svg'
	# Read icon (Just the path line)
	f = codecs.open(image_url ,'r', encoding='utf-8')
	f.readline()
	day['icon'] = f.readline()
	f.close()

	for k, v in day.items():
		output = output.replace('DAY_%d_%s' % (i, k), v)


# Write output
args.output.truncate()
args.output.write(output)
