"""
STATUS: ok
"""

from functions import *
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


def key_regex_type(element):
    if case1.search(element.get("k")):
        case1_keys.add(element.get("k"))
    elif case2.search(element.get("k")):
        case2_keys.add(element.get("k"))
    elif case3.search(element.get("k")):
        case3_keys.add(element.get("k"))
    else:
        good_keys.add(element.get("k"))


def key_regex_validation():
    for element in get_element('tags'):
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
