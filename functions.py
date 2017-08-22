"""
This is the HEART of my project. I'll keep all my repetitive functions here and use them in the subsequent files
"""
import xml.etree.ElementTree as ET
from collections import defaultdict
import os
import string
import re
import unidecode

# todo: Sync the body with Notebook (done)
# todo: Comment the whole code (done)

# Definition of default OSM_FILE location
OSM_FILE = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), 'maps_uncompressed')),
                        "custom_kolkata.osm")

"""
FUNCTION: get_element
STATUS: ok
"""


# Helper function to yield element if it is the right type of tag
def get_element(tags):
    context = iter(ET.iterparse(OSM_FILE, events=('start', 'end')))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()


"""
FUNCTION: get_key_value
STATUS: ok
"""


# Helper function to generate key-value pair of tag(s)
# Usage: For auditing purpose, this generates all the possible distinct values of tag(s) along with the key(s)
def get_key_value(tag, key):
    pair = defaultdict(set)  # all the values are stored as a set to a key
    for elem in get_element(tag):
        if elem.get('k') in key:
            pair[elem.get('k')].add(elem.get('v'))
    return pair


"""
FUNCTION: get_key_modified_value
STATUS: 
"""


# Helper function to generate key-modified:value pair of a tag
# Usage: For auditing purpose, it generates all wrangled values of tag(s) along with the key(s)
def get_key_modified_value(tag, key):
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


"""
FUNCTION: get_modified_value
STATUS: 
"""


# Helper function to return wrangled value of a key for entry in JSON
# Usage: json_maker will call this function to modify the values before creating the JSON
def get_modified_value(k, v):
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


"""
FUNCTION: get_modified_key
STATUS: 
"""


# Helper function to return wrangled key for entry in JSON
# Usage: Returns the modified key when a key is passed and detected in the mapping
def get_modified_key(k):
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

"""
HELPER FUNCTIONS TO WRANGLE THE DATA
"""


# Helper function for general replacements based on map
# STATUS: ok
def fix_replacement(val):
    if val in map_tag_value:
        val = map_tag_value[val]
    return val


# Helper function for lowercase conversion
# STATUS: ok
def fix_lowercase(val):
    return val.lower()


# Helper function for capitalization of each word
# STATUS: ok
def fix_park(val):
    return string.capwords(val)


# Helper function to fix addr:city
# STATUS: ok
def fix_addr_city(city):
    city = fix_replacement(city)  # Replace mapping for wrong/duplicate entries
    city = string.capwords(city)  # Normalize the string to capitalize each word
    city = city.replace(",kolkata", ", Kolkata")
    return city


# Helper function to fix addr:housename
# STATUS: ok
def fix_addr_housename(val):
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


# Helper function to fix addr:housenumber
# STATUS: ok
def fix_addr_housenumber(val):
    if isinstance(val, unicode):
        val = unidecode.unidecode(val)
    val = re.sub(r'[^\w\+\/\&\.\- ]', '', val)
    return val


# Helper function to fix addr:postcode
# STATUS: ok
def fix_addr_postcode(val):
    if isinstance(val, unicode):
        val = unidecode.unidecode(val)
    val = re.sub(r'[ ]', '', val)
    if len(val) < 6:
        val = re.sub(r'0', '00', val, 1)
    if len(val) > 6:
        val = re.sub(r'00', '0', val, 1)
    return val


def fix_addr_state(val):
    return fix_replacement(val)


# Helper function to fix addr:street
# STATUS: ok
def fix_addr_street(val):
    a = val.split(" ")
    a[-1] = fix_replacement(a[-1])
    val = " ".join(a)
    val = string.capwords(val)
    return val


# Helper function to fix brand
def fix_brand(val):
    return fix_replacement(val)


# Helper function to fix is_in
def fix_is_in(val):
    return fix_replacement(val)


# Helper function to fix is_in:country
def fix_is_in_country(val):
    return string.capwords(val)


# Helper function to fix is_in:state
def fix_is_in_state(val):
    return fix_replacement(val)


# Helper function to fix name and name:xx
def fix_name(val):
    if isinstance(val, unicode):
        val = unidecode.unidecode(val)
    return string.capwords(val)


def fix_keys(val):
    if val in map_tag_key:
        return map_tag_key[val]
    else:
        return val
