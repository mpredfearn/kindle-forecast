#!/bin/sh

cd "$(dirname "$0")"

OUT="weather-script-output.png"

SRC="http://YOUR_SERVER/$OUT"

rm -f $OUT

stop framework

lipc-set-prop -i com.lab126.powerd preventScreenSaver 1
lipc-set-prop com.lab126.pillow disableEnablePillow disable

if wget -O $OUT $SRC; then
	eips -f -g $OUT
else
	sleep 60
	if wget -O $OUT $SRC; then
	eips -f -g $OUT
	else
	eips -f -g weather-image-error.png
	fi

fi
