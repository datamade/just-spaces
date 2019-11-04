import os
import sys
import csv

import yaml
from census import Census

from states import STATES, US


class ACSWriter(object):
    """
    Thin wrapper around a csv.DictWriter to perform some common formatting
    for ACS API responses.
    """
    def __init__(self, output, variables):
        """
        - output: A file-like object to write the CSV to
        - variables: A dict of ACS variables parsed from a .config file
                     (see variables.yml for an example)
        """
        self.codes_to_names = {var['code']: var['name'] for var in variables}
        fieldnames = ['fips'] + [var['name'] for var in variables]
        self.writer = csv.DictWriter(output, fieldnames=fieldnames)

    def writeheader(self):
        self.writer.writeheader()

    def write_acs_row(self, fips, acs_row):
        row = {'fips': fips}
        for var_code, var_stat in acs_row.items():
            # Skip fields that don't match queried variables
            if var_code not in self.codes_to_names.keys():
                continue
            # Process nulls
            if var_stat == -666666666:
                var_stat = None

            row[self.codes_to_names[var_code]] = var_stat

        self.writer.writerow(row)


if __name__ == '__main__':
    # Parse ACS variables from the config file
    with open('./variables.yml') as variables_file:
        variables_yml = yaml.load(variables_file)

    # Parse variable argument from the command line
    try:
        census_var = sys.argv[1]
    except IndexError:
        raise NameError('import_acs_data.py requires an ACS variable argument')

    if census_var not in variables_yml.keys():
        msg = (f'Variable {census_var} not valid, must be one of:'
               f' {list(variables_yml.keys())}')
        raise NameError(msg)

    variables = variables_yml[census_var]['variables']
    codes = [var['code'] for var in variables]

    # Parse year from the command line
    try:
        year = sys.argv[2]
    except IndexError:
        raise NameError('import_acs_data.py requires a year argument')

    year = int(year)

    # Init CSV writer object
    writer = ACSWriter(sys.stdout, variables)
    writer.writeheader()

    # Init Census API object
    c = Census(os.environ['CENSUS_API_KEY'], year=year)

    # Import national-level data
    us_res = c.acs5.us(codes)
    assert len(us_res) > 0
    for row in us_res:
        writer.write_acs_row(US, row)

    # Import data for each state
    for state_fips, variables in STATES.items():
        regions = variables['regions']

        # State-level data
        state_res = c.acs5.state(codes, state_fips)
        assert len(state_res) > 0
        for row in state_res:
            writer.write_acs_row(state_fips, row)

        # County-level data
        for region_name, region_vars in regions.items():
            county_fips_codes = region_vars['counties']
            for county in county_fips_codes:
                county_res = c.acs5.state_county(codes, state_fips, county)
                assert len(county_res) > 0
                for row in county_res:
                    writer.write_acs_row(state_fips + county, row)

                # Tract-level data
                tract_res = c.acs5.state_county_tract(codes, state_fips, county, '*')
                assert len(tract_res) > 0
                for row in tract_res:
                    fips = state_fips + county + row['tract']
                    writer.write_acs_row(fips, row)

                # Blockgroup-level data
                block_res = c.acs5.state_county_blockgroup(codes, state_fips, county, '*')
                assert len(block_res) > 0
                for row in block_res:
                    fips = state_fips + county + row['tract'] + row['block group']
                    writer.write_acs_row(fips, row)
