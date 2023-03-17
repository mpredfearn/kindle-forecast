import base64, datetime, logging, matplotlib, requests, tempfile, urllib

from scipy.interpolate import make_interp_spline

import matplotlib.dates as dates
import matplotlib.pyplot as plt
import numpy as np

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)

class Tide(object):
    def __init__(self, tide_time, tide_type, height):
        self.time = tide_time # In GMT
        self.type = tide_type
        self.height = height

    def to_xml(self):
        top = ET.Element("tide")
        # Discarding TZ info on save as strptime imports tz in a different format
        top.attrib["time"] = self.time.strftime("%Y-%m-%dT%H:%M:%S")
        top.attrib["type"] = self.type
        top.attrib["height"] = "%.1f" % self.height

        return top

    def __str__(self):
        return "%s tide (%.2fm) at %s" % (self.type, self.height, self.time)


class TideParser(object):
    """
    Parses the UKHO RSS feed to something less crap.  BeautifulSoup4 is depending on
    LXML as RSS is XML, but the HTML in the RSS needs extracting.
    No errors are handled yet, Requests could return ConnectionError or Timeout
    Location ID is pulled manually from the EasyTide system
    """

    def __init__(self, location_id):
        self.prediction_url = "https://easytide.admiralty.co.uk/Home/GetPredictionData"

        self.location_id = location_id
        self.params = {"stationId": location_id}
        self.tides = []
        self.graph = ""
        self.location = "Unknown"

    def fetch(self):
        sess = requests.Session()

        rsp = sess.get("https://easytide.admiralty.co.uk/Home/GetStations")

        if rsp.status_code == requests.codes.ok:
            #print(rsp.json())
            for station in rsp.json()["features"]:
                #print(station)
                if station["properties"]["Id"] == self.location_id:
                    self.location = station["properties"]["Name"] + ", " + station["properties"]["Country"]
        else:
            rsp.raise_for_status()

        rsp = sess.get(self.prediction_url, params = self.params)
        if rsp.status_code == requests.codes.ok:
            #print(rsp.json())
            times = []
            heights = []
            for event in rsp.json()["tidalEventList"]:
                #print(event)

                t = datetime.datetime.fromisoformat(event["dateTime"])
                self.tides.append(Tide(t, {0: "High", 1: "Low"}[event["eventType"]], event["height"]))

                if t < datetime.datetime.now() + datetime.timedelta(days=2):
                    times.append(t)
                    heights.append(event["height"])
            #print(self.tides)

            num_dates = dates.date2num(times)
            xnew = np.linspace(num_dates.min(), num_dates.max(), 300)
            spl = make_interp_spline(num_dates, heights, k=3)
            plt_heights = spl(xnew)
            plt_dates = dates.num2date(xnew)

            fig, axes = plt.subplots()
            fig.set_size_inches(6,4)
            plt.plot(plt_dates,plt_heights)
            axes.xaxis.set_major_formatter(dates.DateFormatter('%d %b %H:%M'))
            fig.autofmt_xdate()

            tmp = tempfile.NamedTemporaryFile()
            fig.savefig(tmp.name, format="png", dpi=100)

            with open(tmp.name, "rb") as imageFile:
                self.graph = base64.b64encode(imageFile.read()).decode('utf-8')

            #print(self.graph)
            #plt.plot(heights)
            #plt.show()
        else:
            rsp.raise_for_status() 
    
if __name__ == "__main__":
    t = TideParser("0478")
    t.fetch()
    print("Location", t.location)
    for t in t.tides:
        print (t)
