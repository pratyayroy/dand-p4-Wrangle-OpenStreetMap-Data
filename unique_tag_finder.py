"""
STATUS: ok
"""

from functions import *


def find_tag_key():
    unique = set()
    for element in get_element('tag'):
        unique.add(element.get('k'))
    return unique


def test():
    unique_tag_key = find_tag_key()
    print "----------------------------------------------------------------"
    print "The list of UNIQUE TAG KEYs ARE AS FOLLOWS (contains {} entries)".format(len(unique_tag_key))
    print "----------------------------------------------------------------"
    print unique_tag_key


test()
