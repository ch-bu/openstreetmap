from pymongo import MongoClient
import sys
import re
import os
import xml.etree.cElementTree as ET
from xml.etree.cElementTree import iterparse

class OSMClass(object):
    """Base class for parsing the OSM data"""
    def __init__(self, client, filename):
        self.client = client
        self.filename = filename

        # Create database object
        self.elements = self.client['elements']

        # Create collections
        self.nodes = self.elements.nodes
        self.ways = self.elements.ways
        self.relations = self.elements.relations

    def count_tags(self):
        """Counts the number of tags in the map"""
        # Build parsetree
        context = iter(iterparse(self.filename, events=('start', 'end')))
        event, root = next(context)

        tag_dic = {}

        for event, elem in context:
            if event == "start":
                if elem.tag not in tag_dic:
                    tag_dic[elem.tag] = 1
                else:
                    tag_dic[elem.tag] += 1

        return tag_dic


    def parse(self):
        """Parse the xml file"""

        print('Parsing ...')

        # Build parsetree
        context = iter(iterparse(self.filename, events=('start', 'end')))
        event, root = next(context)

        n = 0
        for event, elem in context:
            if event == "start":
                # Add elements to mongo database
                if elem.tag == "node":
                    self.__insert_into_collection__(self.nodes, elem)
                elif elem.tag == "way":
                    self.__insert_into_collection__(self.ways, elem)
                elif elem.tag == "relation":
                    self.__insert_into_collection__(self.relations, elem)

        print('Parsing completed')
            # n += 1
            # if n > 31800:
            #     break
        return None


    def __insert_into_collection__(self, collection, element):
        """Insert an element into a collection"""
        attrib = element.attrib
        regex_colon = re.compile(':')
        problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

        # print("Insert: {}".format(element))

        element_to_insert = {
            "id": attrib['id'],
            "type": element.tag,
            "visible": "true",
            "created": {
                "version": attrib['version'],
                "changeset": attrib['changeset'],
                "user": attrib['user'].replace('.', '_'),
                "uid": attrib['uid']
            }}

        # Add position if tag == node
        if element.tag == "node":
            element_to_insert["pos"] = [float(attrib.get('lon', None)),
                        float(attrib.get('lat', None))]

        # Loop over every tag in element
        for tag in element:
            # Some tags do not contain a k element
            # avoid them
            try:
                # Do not process tags with problematic k key
                if not problemchars.search(tag.attrib['k']):
                    # Key contains information separated by colon -> :
                    if regex_colon.search(tag.attrib['k']) and tag.tag == "tag":

                        splitted = re.split(':', tag.attrib['k'])

                        # Insert key if non-existent
                        if splitted[0] not in element_to_insert:
                            element_to_insert[splitted[0]] = {}

                            # Create nested dictionary if non-existent
                            if splitted[1] not in element_to_insert[splitted[0]]:
                                element_to_insert[splitted[0]][splitted[1]] = {}

                            # Add information of sub dictionary
                            element_to_insert[splitted[0]][splitted[1]] = \
                                tag.attrib['v'].replace('.', '_')
                    # Other key information
                    else:
                        element_to_insert[tag.attrib['k'].replace('.', '_')] = \
                            tag.attrib['v'].replace('.', '_')
                else:
                    print("We found a problematic key: {}".format(tag.attrib['k']))
            except KeyError:
                pass

            # Redesign nd refs. Put them into an list
            if tag.tag == "nd":
                # If node_refs non-existent create empty list
                if "node_refs" not in element_to_insert:
                    element_to_insert['node_refs'] = []

                # Append ref to list
                element_to_insert['node_refs'].append(tag.attrib['ref'])

        # Insert node to node collection
        collection.insert_one(element_to_insert)


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

    print(handler.count_tags())
    handler.parse()
