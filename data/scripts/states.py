# Relevant FIPS codes for geographic queries
US = '1'
# County codes are determined from CBSAs using the following crosswalk:
# https://www.uspto.gov/web/offices/ac/ido/oeip/taf/cls_cbsa/cbsa_countyassoc.htm#PartA1
# Region centroids are found by searching "${city} coordinates" for the primary
# city in each region. Zoom levels are configurable as a separate parameter for
# cases where the region is too large to fit the default zoom level, 11.
# Even though regions can span multiple states, each instance of the 'region'
# dictionary should have its own centroid and default_zoom -- this is necessary
# in order to support Python <3.6, where dictionaries are unordered by default.
STATES = {
    '42': {  # The FIPS code of the state
        'name': 'Pennsylvania',  # The name of the state
        'regions': {
            'Philadelphia': {  # The name of the region
                'counties': ['101'],  # FIPS codes for counties comprising this reigon
                'default_zoom': 11,  # Default map zoom level for this region
                'centroid': (40, -75.16),  # Coordinate center point of this region
            },
            'New York City': {
                'counties': ['103'],
                'default_zoom': 11,
                'centroid': (40.71, -74.00),
            },
        },
    },
    '39': {
        'name': 'Ohio',
        'regions': {
            'Akron': {
                'counties': ['133', '153'],
                'default_zoom': 11,
                'centroid': (41.08, -81.52),
            },
        },
    },
    '13': {
        'name': 'Georgia',
        'regions': {
            'Atlanta': {
                'counties': ['013', '015', '035', '045', '057', '063', '067', '077',
                             '085', '089', '097', '113', '117', '121', '135', '143',
                             '149', '151', '159', '171', '199', '217', '223', '227',
                             '231', '247', '255', '297'],
                'default_zoom': 11,
                'centroid': (33.75, -84.39),
            },
            'Macon, GA': {
                'counties': ['021', '079', '169', '207', '289'],
                'default_zoom': 11,
                'centroid': (32.84, -83.63),
            },
        },
    },
    '25': {
        'name': 'Massachussetts',
        'regions': {
            'Boston': {
                'counties': ['009', '017', '021', '023', '025'],
                'default_zoom': 11,
                'centroid': (42.36, -71.06),
            },
        },
    },
    '33': {
        'name': 'New Hampshire',
        'regions': {
            'Boston': {
                'counties': ['015', '017'],
                'default_zoom': 11,
                'centroid': (42.36, -71.06),
            },
        },
    },
    '37': {
        'name': 'North Carolina',
        'regions': {
            'Charlotte': {
                'counties': ['007', '025', '071', '119', '179'],
                'centroid': (35.23, -80.84),
                'default_zoom': 11
            },
        },
    },
    '45': {
        'name': 'South Carolina',
        'regions': {
            'Charlotte': {
                'counties': ['091'],
                'centroid': (35.23, -80.84),
                'default_zoom': 11
            },
        },
    },
    '17': {
        'name': 'Illinois',
        'regions': {
            'Chicago': {
                'counties': ['031', '037', '043', '063', '089',
                             '093', '097', '111', '197'],
                'default_zoom': 11,
                'centroid': (41.88, -87.63),
            },
        },
    },
    '18': {
        'name': 'Indiana',
        'regions': {
            'Chicago': {
                'counties': ['073', '089', '111', '127'],
                'default_zoom': 11,
                'centroid': (41.88, -87.63),
            },
            'Louisville, KY': {
                'counties': ['019', '043', '061', '175'],
                'default_zoom': 11,
                'centroid': (38.25, -85.76),
            },
        },
    },
    '55': {
        'name': 'Wisconsin',
        'regions': {
            'Chicago': {
                'counties': ['059'],
                'default_zoom': 11,
                'centroid': (41.88, -87.63),
            },
            'Minneapolis-Saint Paul': {
                'counties': ['093', '109'],
                'default_zoom': 11,
                'centroid': (44.94, -93.20),
            },
        },
    },
    '48': {
        'name': 'Texas',
        'regions': {
            'Dallas-Fort Worth': {
                'counties': ['085', '113', '119', '121', '139', '231',
                             '251', '257', '367', '397', '439', '497'],
                'default_zoom': 11,
                'centroid': (32.71, -96.92),
            },
            'Houston': {
                'counties': ['015', '039', '071', '157', '167', '201', '291',
                             '339', '407', '473'],
                'default_zoom': 11,
                'centroid': (29.76, -95.37),
            },
        },
    },
    '26': {
        'name': 'Michigan',
        'regions': {
            'Detroit': {
                'counties': ['087', '093', '099', '125', '147', '163'],
                'default_zoom': 11,
                'centroid': (42.33, -83.05),
            },
            'Lansing, MI': {
                'counties': ['037', '045', '065'],
                'default_zoom': 11,
                'centroid': (42.73, -84.56),
            },
        },
    },
    '29': {
        'name': 'Missouri',
        'regions': {
            'Kansas City': {
                'counties': ['013', '025', '037', '047', '049', '095', '107',
                             '165', '177'],
                'default_zoom': 11,
                'centroid': (39.01, -94.58),
            },
        },
    },
    '20': {
        'name': 'Kansas',
        'regions': {
            'Kansas City': {
                'counties': ['059', '091', '103', '107', '121', '209'],
                'default_zoom': 11,
                'centroid': (39.01, -94.58),
            },
        },
    },
    '06': {
        'name': 'California',
        'regions': {
            'Los Angeles': {
                'counties': ['037', '059'],
                'default_zoom': 11,
                'centroid': (34.05, -118.24),
            },
            'San Francisco': {
                'counties': ['001', '013', '041', '075', '081'],
                'default_zoom': 11,
                'centroid': (37.83, -122.29),
            },
            'San Jose': {
                'counties': ['069', '085'],
                'default_zoom': 11,
                'centroid': (37.34, -121.89),
            },
        },
    },
    '21': {
        'name': 'Kentucky',
        'regions': {
            'Louisville, KY': {
                'counties': ['029', '103', '111', '163', '179', '185', '211',
                             '215', '223'],
                'default_zoom': 11,
                'centroid': (38.25, -85.76),
            },
        },
    },
    '12': {
        'name': 'Florida',
        'regions': {
            'Miami': {
                'counties': ['011', '086', '099'],
                'default_zoom': 11,
                'centroid': (25.76, -80.19),
            },
        },
    },
    '27': {
        'name': 'Minnesota',
        'regions': {
            'Minneapolis-Saint Paul': {
                'counties': ['003', '019', '025', '037', '053', '059', '123',
                             '139', '141', '163', '171'],
                'default_zoom': 11,
                'centroid': (44.94, -93.20),
            },
        },
    },
    '34': {
        'name': 'New Jersey',
        'regions': {
            'New York City': {
                'counties': ['003', '013', '017', '019', '023', '025', '027',
                             '029', '031', '035', '037', '039'],
                'default_zoom': 11,
                'centroid': (40.71, -74.00),
            },
        },
    },
    '36': {
        'name': 'New York',
        'regions': {
            'New York City': {
                'counties': ['005', '047', '059', '061', '079', '081', '085',
                             '087', '103', '119'],
                'default_zoom': 11,
                'centroid': (40.71, -74.00),
            },
        },
    },
    '53': {
        'name': 'Washington',
        'regions': {
            'Seattle': {
                'counties': ['033', '053', '061'],
                'default_zoom': 11,
                'centroid': (47.61, -122.33),
            },
        },
    },
    '11': {
        'name': 'District of Columbia',
        'regions': {
            'Washington, DC': {
                'counties': ['001'],
                'default_zoom': 11,
                'centroid': (38.91, -77.04),
            },
        },
    },
    '24': {
        'name': 'Maryland',
        'regions': {
            'Washington, DC': {
                'counties': ['009', '017', '021', '031', '033'],
                'default_zoom': 11,
                'centroid': (38.91, -77.04),
            },
        },
    },
    '51': {
        'name': 'Virginia',
        'regions': {
            'Washington, DC': {
                'counties': ['013', '043', '059', '061', '107', '153', '177',
                             '179', '187', '510', '600', '610', '630', '683',
                             '685'],
                'default_zoom': 11,
                'centroid': (38.91, -77.04),
            },
        },
    },
    '54': {
        'name': 'West Virginia',
        'regions': {
            'Washington, DC': {
                'counties': ['037'],
                'default_zoom': 11,
                'centroid': (38.91, -77.04),
            },
        },
    },
}

# Create a condensed map associating regions with their counties by merging
# across states.
REGIONS = {}
# Create a map associating counties with their region (the reverse of REGIONS).
COUNTY_TO_REGION = {}
for state, variables in STATES.items():
    state_name = variables['name']
    for region, region_vars in variables['regions'].items():
        if not REGIONS.get(region):
            REGIONS[region] = {
                'counties': [],
                'default_zoom': region_vars['default_zoom'],
                'centroid': region_vars['centroid']
            }
        counties = region_vars['counties']
        REGIONS[region]['counties'].extend(
            [state + county_fips for county_fips in counties]
        )
        for county in counties:
            COUNTY_TO_REGION[state + county] = region
