import sys
import csv
import os
import json


if __name__ == '__main__':
    # Parse input files from the command line
    filenames = sys.argv[1:]
    if len(filenames) == 0:
        raise NameError(
            'One or more arguments representing the files to transform are required'
        )

    fieldnames = ['fips', 'variable', 'fields']
    writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
    writer.writeheader()

    for filename in filenames:
        with open(filename) as fobj:
            reader = csv.reader(fobj)
            header = next(reader)
            columns = header[1:]  # Everything after the first field represents data

            for row in reader:
                out = {}
                out['fips'] = row[0]
                out['variable'] = os.path.basename(filename).split('.csv')[0]
                fields = {}
                for column, value in zip(columns, row[1:]):
                    if value != '':
                        fields[column] = float(value)
                    else:
                        fields[column] = value
                out['fields'] = json.dumps(fields)
                writer.writerow(out)
