FROM httpd:2.4

RUN apt-get -y update
RUN apt-get -y install librsvg2-bin pngcrush python3 python3-bs4 python3-requests python3-tz 

COPY ./cgi-bin /usr/local/apache2/cgi-bin/
RUN chmod +x /usr/local/apache2/cgi-bin/tides.py /usr/local/apache2/cgi-bin/weather.py

COPY ./httpd.conf /usr/local/apache2/conf/httpd.conf
