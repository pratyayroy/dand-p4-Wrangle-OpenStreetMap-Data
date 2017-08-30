"""
This script parses the OSM XML to return a statistics on the number of NODEs, WAYs, RELATIONs, NDs, MEMBERs and TAGs
"""

from functions import *
import pprint


def count_tags():
    tags = {}
    for elem in get_element(('node', 'way', 'relation', 'nd', 'member', 'tag')):
        if elem.tag in tags:
            tags[elem.tag] += 1  # if the tag is encountered then increment it's count by 1
        else:
            tags[elem.tag] = 1  # else flag the tag as encountered and mark it's count as 1
    return tags


# print the tag counts
def test():
    tags = count_tags()
    pprint.pprint(tags)


test()
