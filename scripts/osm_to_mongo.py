from pymongo import MongoClient
import sys
import os
import xml.etree.cElementTree as ET

class OSMClass(object):
    """Base class for parsing the OSM data"""
    def __init__(self, client, filename):
        self.client = MongoClient
        self.filename = filename

    def parse(self):
        """Parse the xml file"""
        print(self.filename)
        # tree = ET.parse(self.filename)

        tree = ET.iterparse(self.filename)
        print(tree.getroot())


if __name__ == "__main__":
    # Check if user had at least to arguments
    if len(sys.argv) != 2:
        print("Usage: %s <OSM file>" % (sys.argv[0]))
        sys.exit(-1)

    # Path of osm file
    filename = sys.argv[1]

    # Check if file exists
    if not os.path.exists(filename):
        print "File %s doesn't exist." % (filename)
        sys.exit(-1)

    # Open mongodb
    client = MongoClient('localhost:27017')

    # Init OSMClass
    handler = OSMClass(client, filename)

    handler.parse()
