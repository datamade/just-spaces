# Relevant FIPS codes for geographic queries
US = '1'
# County codes are determined from CBSAs using the following crosswalk:
# https://www.uspto.gov/web/offices/ac/ido/oeip/taf/cls_cbsa/cbsa_countyassoc.htm#PartA1
# Region centroids are found by searching "${city} coordinates" for the primary
# city in each region. Zoom levels are configurable as a separate parameter for
# cases where the region is too large to fit the default zoom level, 11.
STATES = {
    '42': {
        'name': 'Pennsylvania',
        'regions': {
            'Philadelphia': {
                'counties': ['101'],
                'default_zoom': 11,
                'centroid': (40, -75.16),
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
            },
        },
    },
    '55': {
        'name': 'Wisconsin',
        'regions': {
            'Chicago': {
                'counties': ['059'],
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
