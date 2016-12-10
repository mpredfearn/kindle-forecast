#!/bin/sh

cd "$(dirname "$0")"

OUT="weather.png"

SRC="http://YOURSERVER/cgi-bin/weather.py?code=YAHOOWEATHERCODE"

source ./download-common.sh
