FROM httpd:2.4

RUN apt-get update && apt-get install -y \
	librsvg2-bin \
	python3-matplotlib \
	python3-scipy \
	pngcrush \
	python3-requests

COPY ./cgi-bin /usr/local/apache2/cgi-bin/
RUN chmod +x /usr/local/apache2/cgi-bin/tides.py /usr/local/apache2/cgi-bin/weather.py

COPY ./httpd.conf /usr/local/apache2/conf/httpd.conf
