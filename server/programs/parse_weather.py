#!/usr/bin/env python3
import urllib.request, urllib.parse
from xml.dom import minidom
import json
import datetime
import codecs
#import argparse
import logging, os, sys, tempfile

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)

# Code of my city, if you don't know what to do here, read the README
CODE = "39292"
# Units should be 'c' or 'f'
UNITS='c'

baseurl = "https://query.yahooapis.com/v1/public/yql?"
yql_query = urllib.parse.quote("select * from weather.forecast where u='" + UNITS + "' and woeid=" + CODE)
yql_url = baseurl + "q=" + yql_query +"&format=json"

logging.debug(yql_url)

weather = urllib.request.urlopen(yql_url)

data = json.loads(codecs.decode(weather.read(), "utf-8"))
logging.debug(data)
forecast = data['query']['results']['channel']['item']['forecast']
logging.debug(forecast)

# Open SVG to process
output = open("icons/template.svg", "r", encoding='utf-8').read()

logging.debug("Forecast:")
logging.debug(forecast)

days = { "Mon": "Monday", "Tue": "Tuesday", "Wed": "Wednesday", "Thu": "Thursday", "Fri": "Friday", "Sat": "Saturday", "Sun": "Sunday" }

for i in range(len(forecast)):
	day = forecast[i]

	day["day"] = days[day["day"]]
	logging.debug("Day:")
	logging.debug(day)

	image_url = 'icons/' + day['code'] + '.svg'
	logging.debug("Using icon %s", image_url)
	
	icon = ""
	# Read icon (Just the path line)
	with codecs.open(image_url ,'r', encoding='utf-8') as f:
		for line in f:
			if "xml version" in line or "DOCTYPE" in line:
				pass
			else:
				icon = icon + line
	day['icon'] = icon
	f.close()

	for k, v in day.items():
		output = output.replace('DAY_%d_%s' % (i, k), v)


# Write output
svg = tempfile.NamedTemporaryFile()
png = tempfile.NamedTemporaryFile()

svg.write(bytes(output, 'UTF-8'))

# Convert svg to png
os.system("rsvg-convert --background-color=white -o %s %s" % (png.name, svg.name))

# Optimize the image for kindle eink
os.system("pngcrush -s -c 0 %s pngout.png" % png.name)

with open("pngout.png", 'rb') as f:
    sys.stdout.buffer.write(f.read())
