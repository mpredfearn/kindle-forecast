import datetime, logging, urllib

from tempfile import NamedTemporaryFile

import pytz
from bs4 import BeautifulSoup
import requests

import xml.etree.ElementTree as ET

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

        self.base_url = "http://www.ukho.gov.uk/easytide/EasyTide/"
        self.prediction_url = self.base_url + "ShowPrediction.aspx"

        self.params = {"PortID": location_id,
                       "PredictionLength": "7",
                       "DaylightSavingOffset": "0",
                       "PrinterFriendly": "true",
                       "HeightUnits": "0",
                       "GraphSize": "10"
                       }
    
        self.location = "Unknown"
        self.tides = []
        self.graph = ""

    def fetch(self):
        sess = requests.Session()
        rsp = sess.get(self.prediction_url, params = self.params)

        if rsp.status_code == requests.codes.ok:
            feed_doc = BeautifulSoup(rsp.content, "html.parser")

            table_list = feed_doc.find_all("table", "HWLWTable")
            year = str(datetime.datetime.now().year)
            SILLY_FORMAT = "%Y, %a %d %b %H:%M"

            ret = []
            
            for table in table_list:
                table_date = table.find('th', 'HWLWTableHeaderCell').text
                tide_types = [x.text.strip() for x in table.find_all('th', 'HWLWTableHWLWCellPrintFriendly')]
                times_heights = [x.text.strip() for x in table.find_all('td')]

                midlen = len(times_heights) >> 1
                tide_times = times_heights[0:midlen]
                heights = [float(h[:-2]) for h in times_heights[midlen:]]
                types = ["Low" if x == "LW" else "High" for x in tide_types]
                times = []
                for time in tide_times:
                    times.append(datetime.datetime.strptime(year + ", " + table_date + " " + time, SILLY_FORMAT))

                # Set to GMT, although when it's saved out, this is lost
                gmt = pytz.timezone("GMT")
                times = [gmt.localize(t) for t in times]

                for tide_tuple in zip(times, types, heights):
                    ret.append(Tide(*tide_tuple))

            self.tides = ret
            
            # Get location name
            location = feed_doc.find("span", {"id": "PredictionSummary1_lblPortDetails"})
            self.location = location.text.strip().title()
            
            # Get tide graph
            graph = feed_doc.find("img", {"class", "PredictionGraph"})
            graph_img = sess.get(self.base_url + graph["src"].split("src=")[-1])
            if graph_img.status_code == requests.codes.ok:
                self.graph = graph_img.content

        else:
            rsp.raise_for_status() 
    
if __name__ == "__main__":
    t = TideParser("0478")
    t.fetch()
    print("Location", t.location)
    for t in t.tides:
        print (t)
