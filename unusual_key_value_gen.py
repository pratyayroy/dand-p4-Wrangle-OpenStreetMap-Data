from functions import *

print "---------------------------------"
print "key-value PAIRS FOR tag of CASE 1"
print "---------------------------------"
print get_key_value('tag', ['AND_a_c',
                            'AND_a_nosr_p',
                            'AND_a_nosr_r',
                            'AND_a_w',
                            'City',
                            'GNS:id',
                            'IR:zone',
                            'IRrouterank',
                            'ISO3166-2',
                            'PARK',
                            'Road',
                            'Tank',
                            'currency:INR'])

print "---------------------------------"
print "key-value PAIRS FOR tag of CASE 2"
print "---------------------------------"
print get_key_value('tag', ['building_1',
                            'foot_1',
                            'is_in:iso_3166_2',
                            'leisure_1',
                            'leisure_2',
                            'phone_1',
                            'phone_2',
                            'phone_3'])

print "---------------------------------"
print "key-value PAIRS FOR tag of CASE 3"
print "---------------------------------"
print get_key_value('tag', ['abandoned:aeroway',
                            'alt_name:eo',
                            'alt_name:pl',
                            'gns:dsg',
                            'gns:uni',
                            'name:abbr',
                            'payment:bitcoin',
                            'place:cca',
                            'ref:new',
                            'ref:old',
                            'seamark:construction',
                            'seamark:information',
                            'seamark:mooring:colour',
                            'seamark:status',
                            'source:tracer'])

print "------------------------------------"
print "key-value PAIRS FOR tag of GOOD KEYs"
print "------------------------------------"
print get_key_value('tag', ['district',
                            'from',
                            'is_capital',
                            'kindergarten',
                            'mini_roundabout',
                            'orphanage',
                            'park',
                            'route_refs',
                            'section',
                            'taluk',
                            'to',
                            'via'])
