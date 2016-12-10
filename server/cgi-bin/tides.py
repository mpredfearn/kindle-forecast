#!/usr/bin/env python3
import logging, os, sys, tempfile
import base64, cgi

sys.path.append("lib")

import TideParser

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)

form = cgi.FieldStorage()
location = form.getvalue("location")

tides = TideParser.TideParser(location)

tides.fetch()

# Open SVG to process
output = open("icons/tides.svg", "r", encoding='utf-8').read()

day = 0
svg_day = 0
svg_tide = 0

output = output.replace("TITLE", "Tide times for %s" % tides.location)

for t in tides.tides:
    if not t.time.day == day:
        day = t.time.day
        svg_day += 1
        svg_tide = 1
        output = output.replace("DAY_%d_DAY" % (svg_day), t.time.strftime("%-d %-b"))
    else:
        svg_tide += 1
    
    tide = "DAY_%d_TIDE_%d" % (svg_day, svg_tide)
    logging.debug(tide)
    
    s = "%s %s (%.2fm)" % ("HW" if t.type == "High" else "LW", t.time.strftime("%H:%M"), t.height)
    
    output = output.replace(tide, s)

for svg_day in range(1,4):
    for svg_tide in range(1,6):
        output = output.replace("DAY_%d_TIDE_%d" % (svg_day, svg_tide), "")


output = output.replace("GRAPH", base64.b64encode(tides.graph).decode())

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
