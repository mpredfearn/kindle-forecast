#!/bin/sh

cd "$(dirname "$0")"

OUT="tides.png"

SRC="http://YOURSERVER/cgi-bin/tides.py?location=UKHOEASYTIDELOCATION"

source ./download-common.sh
