#!/bin/sh

rm -f $OUT

# Enable 3G connection
wancontrol wanon

sleep 30

a=0

while true; do
    if wget -O $OUT $SRC; then
        echo "OK"
        break
    else
        a=`expr $a + 1`
        echo "Error downloading attempt $a"
        if [ $a -eq 10 ]; then
            echo "Setting error image"
            cp weather-image-error.png $OUT
            break
        else
            # Try again in 30 seconds
            sleep 30
        fi
    fi
done

# Disable 3G connection
wancontrol wanoff
