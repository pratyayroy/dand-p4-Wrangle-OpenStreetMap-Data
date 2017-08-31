"""
This is the HEART of my project. I'll keep all my repetitive functions here and use them in the subsequent files
"""
import xml.etree.ElementTree as ET
from collections import defaultdict
import os
import string
import re
import unidecode

# Definition of default OSM_FILE location
OSM_FILE = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), 'maps_uncompressed')),
                        "custom_kolkata.osm")


def get_element(tags):
    """
    yields XML Tree if it is the right type of tag
    :param tags: the list of tags that needs to be searched for
    :return: the XML tree for the tag
    """
    context = iter(ET.iterparse(OSM_FILE, events=('start', 'end')))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()


def get_key_value(tag, key):
    """
    generates key-value pair of the passed tag
    :param tag: the tag whose key-value pairs should be generated
    :param key: the keys whose all available values needs to be recorded
    :return: a default dictionary containing the set of values for passed keys for a particular tag
    """
    pair = defaultdict(set)  # all the values are stored as a set to a key
    for elem in get_element(tag):
        if elem.get('k') in key:
            pair[elem.get('k')].add(elem.get('v'))
    return pair


def get_key_modified_value(tag, key):
    """
    generates key-(modified:value) pair of a tag for auditing
    :param tag: the tag whose key-(modified:value) pairs should be generated
    :param key: the keys whose all available (modified:value) needs to be recorded
    :return: a default dictionary containing the set of (modified:value) for passed keys for a particular tag
    """
    pair = defaultdict(set)
    for elem in get_element(tag):
        if elem.get('k') in key:
            k = elem.get('k')
            v = (elem.get('v'))
            if k == "IR:zone":
                v = fix_replacement(v)
            if k == "PARK":
                v = fix_park(v)
            if k == "access":
                v = v.lower()
            if k == "addr:city":
                v = fix_addr_city(v)
            if k == "addr:housename":
                v = fix_addr_housename(v)
            if k == "addr:housenumber":
                v = fix_addr_housenumber(v)
            if k == "addr:postcode":
                v = fix_addr_postcode(v)
            if k == "addr:state":
                v = fix_addr_state(v)
            if k == "addr:street":
                v = fix_addr_street(v)
            if k == "brand":
                v = fix_brand(v)
            if k == "is_in":
                v = fix_is_in(v)
            if k == "is_in:country":
                v = fix_is_in_country(v)
            if k == "is_in:state":
                v = fix_is_in_state(v)
            if k == "name" or k == "name:en" or k == "old_name":
                v = fix_name(v)
            # print "new: " + str(v)
            pair[k].add(v)
    return pair


def get_modified_value(k, v):
    """
    performs lookup for replacement of old value of a key
    :param k: the key whose key whose (modified:value) should be generated
    :param v: the old value to lookup for a possible (modified:value) match
    :return: the (modified:value) corresponding to the old value of a particular key for "TAG" tag
    """
    if k == "IR:zone":
        v = fix_replacement(v)
    if k == "PARK":
        v = fix_park(v)
    if k == "access":
        v = v.lower()
    if k == "addr:city":
        v = fix_addr_city(v)
    if k == "addr:housename":
        v = fix_addr_housename(v)
    if k == "addr:housenumber":
        v = fix_addr_housenumber(v)
    if k == "addr:postcode":
        v = fix_addr_postcode(v)
    if k == "addr:state":
        v = fix_addr_state(v)
    if k == "addr:street":
        v = fix_addr_street(v)
    if k == "brand":
        v = fix_brand(v)
    if k == "is_in":
        v = fix_is_in(v)
    if k == "is_in:country":
        v = fix_is_in_country(v)
    if k == "is_in:state":
        v = fix_is_in_state(v)
    if k == "name" or k == "name:en" or k == "old_name":
        v = fix_name(v)
    if k == "building:levels":
        v = fix_replacement(k)
    if k == "denomination":
        v = fix_replacement(k)
    return v


def get_modified_key(k):
    """
    performs lookup for replacement of old key
    :param k: the old key to lookup for a possible (modified:key) match
    :return: returns the modified key when a key is passed and detected in the mapping
    """
    if k in map_tag_key:
        return map_tag_key[k]
    else:
        return k


"""
MAPPING OF OLD KEY and NEW KEY
"""

map_tag_key = {
    "City": "city",  # suggestion based on Case 1 (4.3.1)
    "PARK": "park",  # suggestion based on Case 1 (4.3.1)
    "Road": "road",  # suggestion based on Case 1 (4.3.1)
    "IR:zone": "indian_railways:zone",  # suggestion based on Case 1 (4.3.1)
    "IRrouterank": "indian_railways_route_rank",  # suggestion based on Case 1 (4.3.1)
    "Tank": "man_made",  # suggestion based on Case 1 (4.3.1)
    "ISO3166-2": "is_in:iso_3166_2",  # suggestion based on Case 1 (4.3.1)
    "building_1": "internet_access",  # suggestion based on Case 2 (4.3.2)
    "phone_1": "phone:1",  # suggestion based on Case 1 (4.3.2)
    "phone_2": "phone:2",  # suggestion based on Case 2 (4.3.2)
    "phone_3": "phone:3",  # suggestion based on Case 2 (4.3.2)
    "leisure_1": "leisure:1",  # suggestion based on Case 2 (4.3.2)
    "leisure_2": "leisure:2",  # suggestion based on Case 2 (4.3.2)
    "name:abbr": "alt_name",  # suggestion based on Case 2 (4.3.3)
}

"""
MAPPING OF OLD VALUE and NEW VALUE
"""

map_tag_value = {
    "water": "water_tower",  # ONLY key: Tank
    "Wifi": "wlan",  # key: internet_access
    "ER": "eastern_railway",  # key: IR:zone
    "kolkata": "Kolkata",  # key: addr:city
    "DUM DUM CANTT.,KOLKATA": "Dum Dum Cantonment, Kolkata",  # key: addr:city
    "Kolkata, West Bengal": "Kolkata",  # key: addr:city
    "WB": "West Bengal",  # key: addr:city
    "Kolkatta": "Kolkata",  # key: addr:city
    "Saltlake (Bidhannagar)": "Salt Lake, Bidhannagar",  # key: addr:city
    "Salt Lake (Bidhan Nagar)": "Salt Lake, Bidhannagar",  # key: addr:city
    "Salt Lake City, Kolkata": "Salt Lake, Bidhannagar",  # key: addr:city
    "Salt Lake": "Salt Lake, Bidhannagar",  # key: addr:city
    "Salt Lake (Bidhannagar)": "Salt Lake, Bidhannagar",  # key: addr:city
    "New Town": "New Town, Rajarhat",  # key: addr:city
    "New Town, Kolkata": "New Town, Rajarhat",  # key: addr:city
    "Newtown, Kolkata": "New Town, Rajarhat",  # key: addr:city
    "Rajarhat": "New Town, Rajarhat",  # key: addr:city
    "(E-W)": "East-West",  # key: addr:street
    "(East)": "East",  # key: addr:street
    "(South)": "South",  # key: addr:street
    "ROAD-PIALI": "Road",  # key: addr:street
    "-Piali": "",  # key: addr:street
    "Road-Piali": "Road",  # key: addr:street
    "Co.Op.": "Co-operative",  # key: addr:street
    "Ln": "Lane",  # key: addr:street
    "Rd": "Road",  # key: addr:street
    "Road(East-West": "Road East-West",  # key: addr:street
    "Road.(S)": "Road South",  # key: addr:street
    "raod": "road",  # key: addr:street
    "IndianOil": "Indian Oil",  # key: brand
    "State Bank of India ATM": "State Bank of India",  # key: brand
    "Kolkata,West Bengal,India": "Kolkata",  # key: is_in
    "State of West Bengal": "West Bengal",  # key: is_in:state
    "1,2,3,4,5": "5",  # key: building:levels
    "2,4,6": "3",  # key: building:levels
    "sive_mandir": "shiv_mandir"  # key: denomination

}


def fix_replacement(val):
    """ for general lookup based on (old_value: new_value) map

    :param val: the value that needs to be searched for
    :return: the modified value if lookup was a hit else the old value
    """
    if val in map_tag_value:
        val = map_tag_value[val]
    return val


def fix_lowercase(val):
    """
    for lowercase conversion
    :param val: the value that needs to be lower-cased
    :return: the modified value
    """
    return val.lower()


def fix_park(val):
    """ for capitalization of each word
    :param val: the string that needs to be cap-worded
    :return: the modified value
    """
    return string.capwords(val)


def fix_addr_city(city):
    """
    to fix addr:city
    :param city: the city name that needs to be fixed
    :return: the modified city
    """
    city = fix_replacement(city)  # Replace mapping for wrong/duplicate entries
    city = string.capwords(city)  # Normalize the string to capitalize each word
    city = city.replace(",kolkata", ", Kolkata")
    return city


def fix_addr_housename(val):
    """
    to fix addr:housename
    :param val: the house-name that needs to be fixed
    :return: the modified house-name
    """
    if isinstance(val, unicode):  # Remove Unicode
        val = unidecode.unidecode(val)
    val = val.replace("WB", "West Bengal")  # Replace shortened state name
    temp = val.split(" ")
    house_number = re.compile(r'^(\w+-\d)|\d|[A-Z][A-Z]')
    if house_number.match(temp[0]):  # Normalizing the string apart form house number
        val = " ".join(temp[1:])
        # val = string.capwords(val)
        val = temp[0] + " " + string.capwords(val)
    else:
        val = string.capwords(val)
    return val


def fix_addr_housenumber(val):
    """
    to fix addr:housenumber
    :param val: the house-number that needs to be fixed
    :return: the modified house-number
    """
    if isinstance(val, unicode):
        val = unidecode.unidecode(val)
    val = re.sub(r'[^\w\+\/\&\.\- ]', '', val)
    return val


def fix_addr_postcode(val):
    """
    to fix addr:postcode
    :param val: the postcode that needs to be fixed
    :return: the modified postcode
    """
    if isinstance(val, unicode):
        val = unidecode.unidecode(val)
    val = re.sub(r'[ ]', '', val)
    if len(val) < 6:
        val = re.sub(r'0', '00', val, 1)
    if len(val) > 6:
        val = re.sub(r'00', '0', val, 1)
    return val


def fix_addr_state(val):
    """
    to fix addr:state
    :param val: the name of the state that needs to be fixed
    :return: the fixed state name
    """
    return fix_replacement(val)


def fix_addr_street(val):
    """
    to fix addr:street
    :param val: the street name that needs modification
    :return: the modified street name
    """
    a = val.split(" ")
    a[-1] = fix_replacement(a[-1])
    val = " ".join(a)
    val = string.capwords(val)
    return val


def fix_brand(val):
    """
    to fix brand names
    :param val: the brand name that needs to be fixed
    :return: the fixed brand name
    """
    return fix_replacement(val)


# Helper function
def fix_is_in(val):
    """
    to fix is_in
    :param val: the is_in value that needs normalization
    :return: the normalized value
    """
    return fix_replacement(val)


def fix_is_in_country(val):
    """
    fix is_in:country
    :param val: the country name that needs normalization
    :return: the normalized country name
    """
    return string.capwords(val)


def fix_is_in_state(val):
    """
    to fix is_in:state
    :param val: the state name that needs to be fixed
    :return: the fixed state name
    """
    return fix_replacement(val)


def fix_name(val):
    """
    to fix name and name:xx
    :param val: the string containing names in different languages
    :return: the fixed name
    """
    if isinstance(val, unicode):
        val = unidecode.unidecode(val)
    return string.capwords(val)


def fix_keys(val):
    """
    to fix the faulty keys
    :param val: the string containing name of the faulty key
    :return: the correct alternative of the key
    """
    if val in map_tag_key:
        return map_tag_key[val]
    else:
        return val
