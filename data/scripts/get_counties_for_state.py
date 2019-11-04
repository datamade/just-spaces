#!/usr/bin/env python3
import sys

from states import STATES


def get_counties(state):
    if state in list(STATES.keys()):
        counties = []
        for region, region_vars in STATES[state]['regions'].items():
            county_codes = region_vars['counties']
            for county in county_codes:
                counties.append(county)
        return counties
    else:
        raise ValueError('FIPS code not recognized: ' + state)


if __name__ == '__main__':
    state = sys.argv[1]
    counties = get_counties(state)
    # Handle SQL syntax (tuples cannot have trailing zeroes, which happens in Python
    # if the tuple only has one element)
    counties_string = str(tuple(counties)).replace(',)', ')')
    sys.stdout.write(counties_string)
