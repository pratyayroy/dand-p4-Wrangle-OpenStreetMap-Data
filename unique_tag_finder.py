"""
This script finds all the unique TAG keys that are used in the OSM XML.
"""

from functions import *


def find_tag_key():
    """
    find all possible keys for the TAG tag
    :return: returns the set containing the unique tags
    """
    unique = set()
    for element in get_element('tag'):  # yield only tags called TAG
        unique.add(element.get('k'))  # store the key of the TAG
    return unique


def test():
    """
    finds the unique tags and prints them
    :return: prints the unique tags
    """
    unique_tag_key = find_tag_key()
    print "----------------------------------------------------------------"
    print "The list of UNIQUE TAG KEYs ARE AS FOLLOWS (contains {} entries)".format(len(unique_tag_key))
    print "----------------------------------------------------------------"
    print unique_tag_key


test()
