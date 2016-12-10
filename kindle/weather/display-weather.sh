#!/bin/sh

cd "$(dirname "$0")"


lipc-set-prop -i com.lab126.powerd preventScreenSaver 1

# Rotate screen
lipc-send-event -r 3 com.lab126.hal orientationLeft

if [ -f state ]; then
    if [ `grep "weather" state` ]; then
        if [ -f weather.png ]; then
            eips -f -g weather.png
        fi
        echo "tides" > state
    elif [ `grep "tides" state` ]; then
        if [ -f tides.png ]; then
            eips -f -g tides.png
        fi
        echo "weather" > state
    else
        echo "weather" > state
    fi
else
    echo "weather" > state
fi

