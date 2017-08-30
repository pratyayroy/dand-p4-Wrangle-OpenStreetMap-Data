"""
This creates a small sample of my .osm file mainly used for familiarization with the data and debugging purposes.
I have included the .osm generated from here "sample1.osm" in maps_uncompressed because of its small size
"""

from functions import *

SAMPLE_FILE = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), 'maps_uncompressed')),
                           "sample1.osm")  # the directory and filename for storing the data

k = 100  # Parameter: take every k-th top level element

with open(SAMPLE_FILE, 'wb') as output:
    output.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    output.write('<osm>\n  ')

    # Write every kth top level element
    for i, element in enumerate(get_element(('node', 'way', 'relation', 'nd', 'member', 'tag'))):
        if i % k == 0:
            output.write(ET.tostring(element, encoding='utf-8'))

    output.write('</osm>')