"""
This script groups the previously found 48 unusual keys into 4 REGULAR EXPRESSION categories based on standards of keys
in OSM wiki. This determines the ones which should be taken care of immediately, and which can be left behind.
"""

import re

"""
We can have the following cases of bad expressions:
1. Presence of any Upper Case Letters (wiki suggests all should be in lowercase)
2. Presence of any special symbols other than ":" and "_"
3. Presence of any colons, <ex: name:en>. We need to fix them for JSON format.

We'll collect the first 2 cases as faulty_tag_keys. We'll deal with case 3 later.
"""

case1 = re.compile(r'[A-Z]')
case2 = re.compile(r'[^a-zA-z:_]')
case3 = re.compile(r'[:]')

case1_keys = set()
case2_keys = set()
case3_keys = set()
good_keys = set()

# I have saved the previous result to save run-time
unusual_tag_key = set(
    ['City', 'PARK', 'via', 'gns:dsg', 'ref:new', 'alt_name:pl', 'ISO3166-2', 'is_capital', 'route_refs', 'foot_1',
     'seamark:mooring:colour', 'IRrouterank', 'seamark:construction', 'phone_2', 'phone_3', 'phone_1',
     'mini_roundabout', 'from', 'district', 'section', 'kindergarten', 'to', 'Road', 'gns:uni', 'GNS:id', 'taluk',
     'Tank', 'seamark:information', 'park', 'building_1', 'abandoned:aeroway', 'name:abbr', 'currency:INR', 'ref:old',
     'payment:bitcoin', 'orphanage', 'IR:zone', 'AND_a_nosr_p', 'AND_a_c', 'AND_a_nosr_r', 'place:cca', 'alt_name:eo',
     'AND_a_w', 'leisure_1', 'leisure_2', 'seamark:status', 'source:tracer', 'is_in:iso_3166_2'])


# based on the detected type, the key is added in its deserved set
def key_regex_type(element):
    if case1.search(element):
        case1_keys.add(element)
    elif case2.search(element):
        case2_keys.add(element)
    elif case3.search(element):
        case3_keys.add(element)
    else:
        good_keys.add(element)


# yielding the tag called TAG and inspecting its key
def key_regex_validation():
    for element in unusual_tag_key:
        key_regex_type(element)


key_regex_validation()
print "----------------------------------------------"
print "TAG KEYS HAVING case 1 (containing {} entries)".format(len(case1_keys))
print "----------------------------------------------"
print case1_keys

print "----------------------------------------------"
print "TAG KEYS HAVING case 2 (containing {} entries)".format(len(case2_keys))
print "----------------------------------------------"
print case2_keys

print "----------------------------------------------"
print "TAG KEYS HAVING case 3 (containing {} entries)".format(len(case3_keys))
print "----------------------------------------------"
print case3_keys

print "-----------------------------------------------"
print "TAG KEYS WHICH ARE good (containing {} entries)".format(len(good_keys))
print "-----------------------------------------------"
print good_keys
