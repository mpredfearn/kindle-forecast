#!/bin/sh

rm -f $OUT

# Enable 3G connection
wancontrol wanon

sleep 30

if wget -O $OUT $SRC; then
echo "OK"
else
	sleep 60
	if wget -O $OUT $SRC; then
        cp weather-image-error.png $OUT
	fi
fi

# Disable 3G connection
wancontrol wanoff
