import os
import csv

import psycopg2
from django.core.management.base import BaseCommand
from django.conf import settings

DB_CONN = 'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}'
DB_CONN_STR = DB_CONN.format(**settings.DATABASES['default'])


class Command(BaseCommand):
    help = 'Load ACS data into the database'

    def handle(self, *args, **kwargs):
        data_dir = os.path.join('data', 'final', 'acs')
        for filename in os.listdir(data_dir):
            if filename.endswith('.csv'):
                filepath = os.path.join(data_dir, filename)
                filename = os.path.basename(filepath).split('.csv')[0]
                tablename = 'acs_{}'.format(filename)
                self.import_csv(filepath, tablename)
                self.stdout.write(self.style.SUCCESS('Imported {}'.format(filepath)))

    def import_csv(self, filepath, tablename):
        """
        Import a CSV file into the database.

        :param filepath: The path to the CSV file to load.
        :param tablename: The name of the table to load.
        """
        with open(filepath, 'r') as fobj:
            reader = csv.reader(fobj)
            header = next(reader)

        # The first field is always the FIPS code, the rest are float variables
        fields = '"{}" VARCHAR,'.format(header[0].lower())
        fields += ', '.join(['"{}" DOUBLE PRECISION'.format(head.lower()) for head in header[1:]])

        copy_st = '''
            COPY {} FROM STDIN WITH CSV HEADER
        '''.format(tablename)

        with open(filepath, 'r') as fobj:
            with psycopg2.connect(DB_CONN_STR) as conn:
                with conn.cursor() as curs:
                    try:
                        curs.execute('''DROP TABLE IF EXISTS {}'''.format(tablename))
                        curs.execute('''
                            CREATE TABLE {0} (
                                {1}
                            )
                        '''.format(tablename, fields))
                        curs.copy_expert(copy_st, fobj)
                    except psycopg2.IntegrityError as e:
                        conn.rollback()
                        raise e
