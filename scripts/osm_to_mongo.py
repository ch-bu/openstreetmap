from pymongo import MongoClient
import sys
import os
import xml.etree.cElementTree as ET
from xml.etree.cElementTree import iterparse

class OSMClass(object):
    """Base class for parsing the OSM data"""
    def __init__(self, client, filename):
        self.client = client
        self.filename = filename

        # Create databases
        self.nodes = self.client['nodes']
        self.users = self.nodes.users
        self.spot = self.nodes.spot

    def parse(self):
        """Parse the xml file"""

        # Build parsetree
        # tree = ET.iterparse(self.filename)
        context = iter(iterparse(self.filename, events=('start', 'end')))
        event, root = next(context)

        n = 0
        for event, elem in context:

            if event == "start":
                print('\n***************************')
                # print(elem.tag)

                if elem.tag == "node":
                    print(elem.attrib)
                    for tag in elem:
                        print(tag)

            elif event == "end":
                print('***************************')

            # for el in elem:
            #     print('****')
            #     print(el)
        #     # if elem.tag == "node":
        #     #     node = elem.attrib
        #     #     print(node['id'])
        #     #     self.spot.insert_one({"node_id": node['id'], "user": node['user'],
        #     #                           "lon": node['lon'], "lat": node['lat'],
        #     #                           "timestamp": node['timestamp']})
        #
            n += 1

            if n > 50:
                break


if __name__ == "__main__":
    # Check if user had at least to arguments
    if len(sys.argv) != 2:
        print("Usage: %s <OSM file>" % (sys.argv[0]))
        sys.exit(-1)

    # Path of osm file
    filename = sys.argv[1]

    # Check if file exists
    if not os.path.exists(filename):
        print("File %s doesn't exist." % (filename))
        sys.exit(-1)

    # Open mongodb
    client = MongoClient('localhost:27017')

    # Init OSMClass
    handler = OSMClass(client, filename)

    handler.parse()
