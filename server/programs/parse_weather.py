import urllib3, urllib
from xml.dom import minidom
import json
import datetime
import codecs


#Code of my city, if you don't know what to do here, read the README
CODE = "39292"

http = urllib3.PoolManager()

#weather = http.request('GET', 'http://weather.yahooapis.com/forecastrss?w=' + CODE + '&u=c')
baseurl = "https://query.yahooapis.com/v1/public/yql?"
yql_query = "q=select%20*%20from%20weather.forecast%20where%20u='c'%20and%20woeid=" + CODE
#yql_query = "select wind from weather.forecast where woeid=" + CODE
#yql_url = baseurl + urllib.urlencode({'q':yql_query}) + "&format=json"
yql_url = baseurl + yql_query +"&format=json"

weather = http.request('GET', yql_url)

#weather_xml = weather.data
#print(weather_xml)
#dom = minidom.parseString(weather_xml)
#print(dom)
#Get weather Tags
#xml_temperatures = dom.getElementsByTagName('yweather:forecast')
print(weather.data)
reader = codecs.getreader("utf-8")
data = json.loads(codecs.decode(weather.data, "utf-8"))
print(data)
xml_temperatures = data['query']['results']['channel']['item']['forecast']
print(xml_temperatures)

#Get today Tag
today = xml_temperatures[0]

#Get info
low = today['low']
high = today['high']
image = today['code']
date = today['date']
image_url = 'icons/' + image + '.svg'

# Open SVG to process
output = codecs.open('icons/template.svg', 'r', encoding='utf-8').read()


#Read icon (Just the path line)
f = codecs.open(image_url ,'r', encoding='utf-8')
f.readline()
icon = f.readline()
f.close()

# Insert icons and temperatures
#output = output.replace('TODAY',date)
output = output.replace('ICON_ONE',icon)
output = output.replace('HIGH_ONE',high)
output = output.replace('LOW_ONE',low)

# Write output
codecs.open('after-weather.svg', 'w', encoding='utf-8').write(output)
