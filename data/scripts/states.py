# Relevant FIPS codes for geographic queries
US = '1'
# County codes are determined from CBSAs using the following crosswalk:
# https://www.uspto.gov/web/offices/ac/ido/oeip/taf/cls_cbsa/cbsa_countyassoc.htm#PartA1
STATES = {
    '42': {
        'name': 'Pennsylvania',
        'regions': {
            'Philadelphia': ['101'],
        },
    },
    '39': {
        'name': 'Ohio',
        'regions': {
            'Akron': ['133', '153'],
        },
    },
    '13': {
        'name': 'Georgia',
        'regions': {
            'Atlanta': ['013', '015', '035', '045', '057', '063', '067', '077',
                        '085', '089', '097', '113', '117', '121', '135', '143',
                        '149', '151', '159', '171', '199', '217', '223', '227',
                        '231', '247', '255', '297']
        }
    },
    '25': {
        'name': 'Massachussetts',
        'regions': {
            'Boston': ['009', '017', '021', '023', '025']
        }
    },
    '33': {
        'name': 'New Hampshire',
        'regions': {
            'Boston': ['015', '017']
        }
    },
    '37': {
        'name': 'North Carolina',
        'regions': {
            'Charlotte': ['007', '025', '071', '119', '179']
        }
    },
    '45': {
        'name': 'South Carolina',
        'regions': {
            'Charlotte': ['091']
        }
    },
    '17': {
        'name': 'Illinois',
        'regions': {
            'Chicago': ['031', '037', '043', '063', '089', '093', '097', '111', '197']
        }
    },
    '18': {
        'name': 'Indiana',
        'regions': {
            'Chicago': ['073', '089', '111', '127']
        }
    },
    '55': {
        'name': 'Wisconsin',
        'regions': {
            'Chicago': ['059']
        }
    },
}

# Create a condensed map associating regions with their counties by merging
# across states.
REGIONS = {}
for state, variables in STATES.items():
    state_name = variables['name']
    for region, counties in variables['regions'].items():
        if not REGIONS.get(region):
            REGIONS[region] = []
        REGIONS[region].extend([state + county_fips for county_fips in counties])
