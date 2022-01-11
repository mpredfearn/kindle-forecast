#!/usr/bin/env python3

import logging, os, sys, tempfile
import cgi

sys.path.append("lib")

import WeatherParser

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)

form = cgi.FieldStorage()
location = form.getvalue("location")

weather = WeatherParser.WeatherParser(location)

output = weather.fetch()

# Write output
svg = tempfile.NamedTemporaryFile()
png = tempfile.NamedTemporaryFile()
out = tempfile.NamedTemporaryFile('rb')

svg.write(bytes(output, 'UTF-8'))

# Convert svg to png
os.system("rsvg-convert --background-color=white -o %s %s" % (png.name, svg.name))

# Optimize the image for kindle eink
os.system("pngcrush -s -c 0 %s %s" % (png.name, out.name))

print("Content-Type: image/png\n")
sys.stdout.flush()
sys.stdout.buffer.write(out.read())
