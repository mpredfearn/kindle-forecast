#!/bin/sh

cd "$(dirname "$0")"

python programs/parse_weather.py --template=icons/template.svg --output=output.svg
#python programs/parse_ical.py

rsvg-convert --background-color=white -o output.png output.svg

#We optimize the image
pngcrush -c 0 -ow output.png

#We move the image where it needs to be
rm -f /home/weather/public_html/huddersfield.png
mv output.png /home/weather/public_html/huddersfield.png

rm output.svg

