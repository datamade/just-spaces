import os
import sys
import csv

import yaml
from census import Census

PA_FIPS = '42'
PHILLY_FIPS = '101'

with open('./variables.yml') as variables_file:
    variables_yml = yaml.load(variables_file)


if __name__ == '__main__':
    try:
        census_var = sys.argv[1]
    except IndexError:
        raise NameError('import_acs_data.py requires an ACS variable argument')

    if census_var not in variables_yml.keys():
        msg = (f'Variable {census_var} not valid, must be one of:'
               f' {list(variables_yml.keys())}')
        raise NameError(msg)

    variables = variables_yml[census_var]['variables']
    fieldnames = ['fips'] + [var['name'] for var in variables]

    writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
    writer.writeheader()

    codes_to_names = {var['code']: var['name'] for var in variables}
    codes = [var['code'] for var in variables]
    c = Census(os.environ['CENSUS_API_KEY'], year=2016)

    # National-level data (always returns only one row, a dict of fields)
    us_res = c.acs5.us(codes)[0]
    us_row = {codes_to_names[code]: stat for code, stat in us_res.items()
              if code in codes_to_names.keys()}
    us_row['fips'] = '1'
    writer.writerow(us_row)

    # State-level data
    pa_res = c.acs5.state(codes, PA_FIPS)[0]
    pa_row = {codes_to_names[code]: stat for code, stat in pa_res.items()
              if code in codes_to_names.keys()}
    pa_row['fips'] = PA_FIPS
    writer.writerow(pa_row)

    # County-level data
    philly_res = c.acs5.state_county(codes, PA_FIPS, PHILLY_FIPS)[0]
    philly_row = {codes_to_names[code]: stat for code, stat in philly_res.items()
                  if code in codes_to_names.keys()}
    philly_row['fips'] = PA_FIPS + PHILLY_FIPS
    writer.writerow(philly_row)

    # Tract-level data
    tract_res = c.acs5.state_county_tract(codes, PA_FIPS, PHILLY_FIPS, '*')
    assert len(tract_res) > 0
    for row in tract_res:
        assert len(row) > 0
        tract_row = {codes_to_names[code]: stat for code, stat in row.items()
                     if code in codes_to_names.keys()}
        tract_row['fips'] = PA_FIPS + PHILLY_FIPS + row['tract']
        writer.writerow(tract_row)

    # Blockgroup-level data
    block_res = c.acs5.state_county_blockgroup(codes, PA_FIPS, PHILLY_FIPS, '*')
    assert len(block_res) > 0
    for row in block_res:
        assert len(row) > 0
        block_row = {codes_to_names[code]: stat for code, stat in row.items()
                     if code in codes_to_names.keys()}
        block_row['fips'] = PA_FIPS + PHILLY_FIPS + row['tract'] + row['block group']
        writer.writerow(block_row)
