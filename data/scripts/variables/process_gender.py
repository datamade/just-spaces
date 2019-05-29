import csv
import sys

output_fields = [
    'under_5', '5_to_9', '10_to_14', '15_to_17', '18_to_19', '20', '21', '22_to_24',
    '25_to_29', '30_to_34', '35_to_39', '40_to_44', '45_to_49', '50_to_54', '55_to_59',
    '60_to_61', '62_to_64', '65_to_66', '67_to_69', '70_to_74', '75_to_79', '80_to_84',
    '85_plus'
]

field_mapping = {field: ['male_' + field, 'female_' + field] for field in output_fields}

if __name__ == '__main__':
    # Parse input files from the command line
    filename = sys.argv[1]
    if len(filename) == 0:
        raise NameError(
            'Script requires an argument representing the file to process'
        )

    with open(filename) as fobj:
        reader = csv.DictReader(fobj)
        writer = csv.DictWriter(sys.stdout, fieldnames=['fips'] + list(field_mapping.keys()))
        writer.writeheader()

        for row in reader:
            output_row = {'fips': row['fips']}
            for output_field, input_fields in field_mapping.items():
                output_row[output_field] = 0
                for input_field in input_fields:
                    output_row[output_field] += float(row[input_field])
            writer.writerow(output_row)
