"""
This script finds all the unique TAG keys that are used in the OSM XML.
"""

from functions import *


def find_tag_key():
    unique = set()
    for element in get_element('tag'):  # yield only tags called TAG
        unique.add(element.get('k'))  # store the key of the TAG
    return unique


# print the unique TAG keys
def test():
    unique_tag_key = find_tag_key()
    print "----------------------------------------------------------------"
    print "The list of UNIQUE TAG KEYs ARE AS FOLLOWS (contains {} entries)".format(len(unique_tag_key))
    print "----------------------------------------------------------------"
    print unique_tag_key


test()
