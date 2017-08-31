#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import json
from functions import *

# todo: Run and Upload to MongoDB
# todo: addr:country not showing India


"""
----------------------
- SAMPLE CONVERSIONS -
----------------------
{
"id": "2406124091",
"type: "node",
"visible":"true",
"created": {
          "version":"2",
          "changeset":"17206049",
          "timestamp":"2013-08-03T16:43:42Z",
          "user":"linuxUser16",
          "uid":"1219059"
        },
"pos": [41.9757030, -87.6921867],
"address": {
          "housenumber": "5157",
          "postcode": "60625",
          "street": "North Lincoln Ave"
        },
"amenity": "restaurant",
"cuisine": "mexican",
"name": "La Cabana De Don Luis",
"phone": "1 (773)-271-5176"
}

-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

<tag k="addr:housenumber" v="5158"/>
<tag k="addr:street" v="North Lincoln Avenue"/>
<tag k="addr:street:name" v="Lincoln"/>
<tag k="addr:street:prefix" v="North"/>
<tag k="addr:street:type" v="Avenue"/>
<tag k="amenity" v="pharmacy"/>
 
            ↓
  should be turned into:
            ↓

{...
"address": {
    "housenumber": 5158,
    "street": "North Lincoln Avenue"
}
"amenity": "pharmacy",
...
}

-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#


  <nd ref="305896090"/>
  <nd ref="1719825889"/>
  
            ↓
  should be turned into:
            ↓
            
"node_refs": ["305896090", "1719825889"]


-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
"""

# Regex to match key values
lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

# arrays to store specific attributes of a node in an array
CREATED = ["version", "changeset", "timestamp", "user", "uid"]  # to be stored as a dictionary to key "created"
POS = ["lat", "lon"]  # to be stored as an array to key "pos"


def shape_element(element):
    """
    main function to convert all attributes and tags of a node/way as a compact dictionary for JSON entry
    :param element: the node/way whose all child tags will be added as key-value pair
    :return: the dictionary containing all the tags of the node/way as key-value
    """
    node = {}  # this dictionary will hold the converted XMLs
    # block applicable to WAY only
    if element.tag == "way":
        node['node_refs'] = []  # this array will store the reference ids inside tag "nd" with key "node_refs"
        for ref in element:
            if ref.tag == "nd":
                node['node_refs'].append(ref.get('ref'))

    # block applicable to NODE only
    if element.tag == "node":
        att = list(element.attrib.keys())
        att = list(set(att) - set(CREATED))
        att = list(set(att) - set(POS))
        for i in att:
            node[i] = element.get(i)  # this will store the attributes of tag "node" other than "created" and "pos"
        node['pos'] = []
        for pos_val in POS:  # this will store the latitude and longitude of tag "node"
            node['pos'].append(float(element.get(pos_val)))

    # block common for both NODE and WAY
    if element.tag == "node" or element.tag == "way":
        node["element_type"] = element.tag  # this will store the element type of the "tag" - NODE or WAY
        node['created'] = {}

        for created_val in CREATED:  # to fill in details of CREATED array as a dictionary
            node['created'][created_val] = element.get(created_val)

        for tags in element:  # to create a dictionary entry for no-colon/perfect keys
            old_key = tags.get('k')
            new_key = get_modified_key(old_key)
            if tags.tag == "tag" and lower.match(new_key):
                node[new_key] = get_modified_value(old_key, tags.get('v'))

        for tags in element:  # to create dictionary entry for multi-level keys
            old_key = tags.get('k')
            new_key = get_modified_key(old_key)
            if tags.tag == "tag" and lower_colon.match(new_key):
                sp = new_key.split(":")  # if keys are not modified, there's no effect else take into account the new
                if len(sp) <= 2 and not problemchars.match(sp[1]):  # only applicable for 2 levels with no problemchar
                    if sp[0] == "addr":  # special treatment for multilevel entry of addr:
                        if "address" not in node:
                            node["address"] = {}  # the value is stored as a dictionary to key "address"
                        node["address"][sp[1]] = get_modified_value(old_key, tags.get('v'))
                    else:
                        if sp[0] not in node:  # if no similar key to the base of this multilevel key exists
                            node[sp[0]] = {}
                        elif not isinstance(node[sp[0]], dict):
                            continue  # if similar key to the base of this multilevel key exists, exiting addition

                        node[sp[0]][sp[1]] = get_modified_value(old_key, tags.get('v'))  # adding the multilevel key
    return node


def process_map(file_in, pretty=False):
    """
    driver function to call a JSON entry and write back to the file
    :param file_in: the OSM file that needs to be converted
    :param pretty: how the JSON will be formed (false makes it compact but not human-friendly)
    :return: the file JSON file is created
    """
    file_out = "{0}.json".format(file_in)

    with codecs.open(file_out, "w") as fo:
        for element in get_element(['node', 'way', 'nd', 'tag']):
            el = shape_element(element)
            if el:
                # data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2) + "\n")
                else:
                    fo.write(json.dumps(el) + "\n")


# call the whole thing
process_map(OSM_FILE, False)
