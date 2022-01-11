import codecs, datetime, json, logging, requests, urllib

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)


class WeatherParser(object):
    """
    Parses the UKHO RSS feed to something less crap.  BeautifulSoup4 is depending on
    LXML as RSS is XML, but the HTML in the RSS needs extracting.
    No errors are handled yet, Requests could return ConnectionError or Timeout
    Location ID is pulled manually from the EasyTide system
    """

    def __init__(self, location_id):

        self.url = "http://api.openweathermap.org/data/2.5/forecast/daily"

        self.params = {"id": location_id,
                       "cnt": "7",
                       "units": "metric",
                       "APPID": "76c7f19f63377822b0c0039d464fbdf1"
                      }


        #self.location = "Unknown"
        #self.tides = []
        #self.graph = ""

    def fetch(self):
        sess = requests.Session()
        rsp = sess.get(self.url, params = self.params)

        if rsp.status_code == requests.codes.ok:
            #logging.debug(rsp.content)
            data = json.loads(codecs.decode(rsp.content, "utf-8"))

            # Open SVG to process
            output = open("icons/template.svg", "r", encoding='utf-8').read()

            #logging.debug("City: %s" % data['city']['name'])
            output = output.replace('LOCATION', data['city']['name'])

            forecast = data['list']
            for i in range(len(forecast)):
                day = {}
                dow = datetime.datetime.fromtimestamp(int(forecast[i]['dt'])).strftime('%A')
                #logging.debug("Day %s" % dow)
                day['day'] = dow

                day['high'] = str(int(forecast[i]['temp']['max']))
                day['low'] = str(int(forecast[i]['temp']['min']))

                image_url = 'icons/' + forecast[i]['weather'][0]['icon'] + '.svg'
                #logging.debug("Using icon %s", image_url)

                icon = ""
                # Read icon (Just the path line)
                with codecs.open(image_url ,'r', encoding='utf-8') as f:
                    for line in f:
                        if "xml version" in line or "DOCTYPE" in line:
                            pass
                        else:
                            icon = icon + line
                day['icon'] = icon
                f.close()

                for k, v in day.items():
                    output = output.replace('DAY_%d_%s' % (i, k), v)

            #logging.debug(output)

        return output



if __name__ == "__main__":
    t = WeatherParser("3333164")
    t.fetch()
