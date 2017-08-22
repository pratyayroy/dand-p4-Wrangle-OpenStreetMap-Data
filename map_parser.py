"""
STATUS: revise
"""

from functions import *
import pprint


def count_tags():
    tags = {}
    for elem in get_element(('node', 'way', 'relation', 'nd', 'member', 'tag')):
        if elem.tag in tags:
            tags[elem.tag] += 1
        else:
            tags[elem.tag] = 1
    return tags


def test():
    tags = count_tags()
    pprint.pprint(tags)


test()
