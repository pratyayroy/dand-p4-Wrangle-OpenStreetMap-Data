"""
This script finds among the UNIQUE TAG KEYs, the ones which do not have a proper wiki in tagsinfo
"""
from bs4 import BeautifulSoup
import requests
import time
# from unique_tag_finder import *

# uncomment the above import to get dynamic unique_tag_key and not the static one as used
# I have used the static one to speed-up. This contains a 359 tag keys found from the previous script
unique_tag_key = set(
    ['maxspeed', 'currency:others', 'IRrouterank', 'seamark:construction', 'is_in', 'seamark:type', 'created_by', 'to',
     'crossing:barrier', 'fax', 'name:ur', 'icao', 'name:uk', 'motor_vehicle', 'addr:street', 'source:name',
     'AND_a_nosr_p', 'level', 'ref', 'nursery', 'protected_area', 'subway', 'is_in:continent', 'source:tracer',
     'sidewalk', 'bicycle', 'name:id', 'fuel:lpg', 'ref:new', 'crop', 'name:is', 'area:highway', 'name:it', 'phone_2',
     'phone_3', 'phone_1', 'cargo', 'seamark:reflectivity', 'section', 'access', 'capital', 'fuel:e85',
     'building:units', 'name:br', 'water', 'name:bn', 'name:bh', 'name:be', 'name:bg', 'fuel:e10', 'name:yo',
     'military', 'name:pt', 'via', 'layer', 'tower:type', 'name:pa', 'name:pl', 'fee', 'from',
     'public_transport:version', 'gns:dsg', 'type', 'start_date', 'seamark:buoy_cardinal:category', 'entrance',
     'name:ro', 'end_date', 'motorroad', 'phone', 'train', 'currency:INR', 'uic_ref', 'fuel:GTL_diesel', 'tunnel',
     'name:ms', 'name:mr', 'lock', 'ISO3166-2', 'name:mg', 'name:ml', 'species', 'name:mk', 'name:fa', 'name:fi',
     'name:fr', 'product', 'iata', 'Tank', 'description', 'district', 'seamark:buoy_cardinal:colour_pattern',
     'fuel:1_50', 'wheelchair', 'outdoor_seating', 'addr:place', 'fuel:cng', 'takeaway', 'restriction', 'office',
     'building:part', 'name:th', 'postal_code', 'motorcycle', 'int_ref', 'source:position', 'name:ta', 'name:tg',
     'name:te', 'mini_roundabout', 'kindergarten', 'fuel:1_25', 'after_school', 'covered', 'junction',
     'seamark:buoy_cardinal:colour', 'cutting', 'foot', 'tourism', 'smoothness', 'ref:old', 'payment:bitcoin', 'fixme',
     'addr:city', 'AND_a_c', 'tram', 'addr:state', 'AND_a_w', 'seamark:conspicuity', 'embankment', 'crossing', 'name_1',
     'name:as', 'name:ar', 'operator', 'frequency', 'loc_name', 'todo', 'building:fireproof', 'name:af', 'network',
     'brand:wikidata', 'name:zh', 'highway', 'name:sk', 'barrier', 'seamark:information', 'electrified', 'name:sa',
     'name:sv', 'name:sr', 'noexit', 'segregated', 'route', 'atm', 'place', 'int_name', 'horse', 'service',
     'addr:housename', 'station', 'name:hi', 'name:he', 'park', 'is_in:state', 'seamark:buoy_cardinal:shape', 'natural',
     'name:hu', 'name:hr', 'Road', 'population', 'AND:importance_level', 'aeroway', 'seamark:mooring:category',
     'landuse', 'bridge', 'addr:suburb', 'generator:method', 'wikidata', 'foot_1', 'seamark:mooring:colour',
     'fuel:electricity', 'addr:district', 'building:levels', 'note', 'mooring', 'fuel:HGV_diesel', 'building:colour',
     'url', 'is_in:iso_3166_2', 'shop', 'golf', 'name:ka', 'name:ko', 'name:kn', 'social_facility', 'name:ku', 'gauge',
     'trail_visibility', 'is_in:city', 'name:tr', 'name:lv', 'name:lt', 'name:cs', 'service_times', 'leisure',
     'name:la', 'name:eo', 'name:en', 'addr:postcode', 'motorboat', 'internet_access:fee', 'public_transport',
     'name:eu', 'name:et', 'ruins', 'name:es', 'is_capital', 'name:tl', 'wetland', 'parking', 'name:ru', 'sport',
     'capacity', 'fuel:diesel', 'wikipedia', 'seamark:buoy_lateral:category', 'boundary', 'email', 'addr:housenumber',
     'contact:email', 'denomination', 'building:use', 'substation', 'land_area', 'orphanage', 'place:cca', 'tracks',
     'leisure_1', 'leisure_2', 'railway', 'seamark:name', 'alt_name:pl', 'seamark:buoy_lateral:system', 'name:oc',
     'community', 'height', 'name:or', 'bench', 'boat', 'bicycle_parking', 'website', 'lanes', 'building_1', 'craft',
     'smoking', 'abandoned', 'alt_name:eo', 'fuel:biogas', 'country', 'railway:traffic_mode', 'City', 'amenity',
     'canoe', 'toilets:disposal', 'surface', 'social_facility:for', 'name:vi', 'waterway', 'cuisine', 'emergency',
     'fuel:octane_98', 'GNS:id', 'fuel:octane_91', 'fuel:octane_95', 'drink', 'fence_type', 'name:abbr', 'intermittent',
     'colour', 'oneway', 'addr:country', 'name:cy', 'PARK', 'drive_through', 'voltage', 'name:ca', 'lit', 'name:da',
     'ele', 'source', 'usage', 'name:dv', 'short_name', 'fuel:biodiesel', 'gns:uni', 'seamark:buoy_lateral:shape',
     'historic', 'name', 'vending', 'designation', 'seamark:buoy_lateral:colour', 'internet_access', 'alt_name',
     'platforms', 'local_ref', 'man_made', 'religion', 'fuel:octane_100', 'name:de', 'artwork_type', 'taluk', 'name:ja',
     'power', 'incline', 'footway', 'supervised', 'aquaculture', 'plant:output:electricity', 'IR:zone',
     'generator:source', 'area', 'unisex', 'opening_hours', 'museum', 'contact:phone', 'width', 'admin_level', 'bus',
     'brand', 'ford', 'delivery', 'construction', 'old_name', 'name:qu', 'passenger_lines', 'route_refs',
     'route_master', 'dispensing', 'seamark:status', 'maxheight', 'ship', 'cables', 'is_in:country', 'cycleway',
     'name:nl', 'name:nn', 'name:no', 'shelter', 'is_in:country_code', 'name:ne', 'min_height', 'seamark:topmark:shape',
     'AND_a_nosr_r', 'building', 'wifi', 'traffic_signals', 'abandoned:aeroway', 'name:gu'])

without_wiki = set()
language_code = set()

# Let's get List of ISO 639 codes to validate multilingual code names from Wikipedia
url = "https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes"
r = requests.get(url)
data = r.text
soup = BeautifulSoup(data, "lxml")
# Stripping the required columns out of the Table in the HTML
table = soup.find("table", {"id": "Table"})
for row in table.find_all("tr"):
    try:
        iso_639_1 = str(row.find_all("td")[4].find("a").text)
        language_code.add(iso_639_1)
        iso_639_2T = str(row.find_all("td")[5].text)
        language_code.add(iso_639_2T)
        iso_639_2B = str(row.find_all("td")[6].text)
        language_code.add(iso_639_2T)
        iso_639_3 = str(row.find_all("td")[7].text.split(" ")[0])
        language_code.add(iso_639_3)
    except:
        continue
print "----------------------------------------------------------------------------"
print "Extracted Language Codes from Wikipedia is as follows: (contains {} entries)".format(len(language_code))
print "----------------------------------------------------------------------------"
print language_code

# for each key of a tag identified, we check if an OSM-wiki exists to validate it's significance
for val in unique_tag_key:
    time.sleep(0.1)
    url = "http://taginfo.openstreetmap.in/keys/"
    r = requests.get(url + val + "#wiki")
    data = r.text
    soup = BeautifulSoup(data, "lxml")
    not_found = False
    for paragraph in soup.find_all("p"):
        # deciding validity based on what the wiki page says
        if paragraph.string.startswith("No wiki page available for this key."):
            not_found = True
            break
    # if the wiki page is not found, we add that to the "without_wiki" list
    if not_found:
        # however before adding we check if the key was a name and absent in "language_code"
        if val.startswith("name:"):
            if val.split(":")[1] in language_code:
                continue
        without_wiki.add(val)

print len(without_wiki)
print without_wiki

print "------------------------------------------------------------"
print "TAG KEYS WITHOUT/WEAK WIKI IN taginfo: (contains {} entries)".format(len(without_wiki))
print "------------------------------------------------------------"
print without_wiki
