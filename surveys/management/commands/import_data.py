import os
import csv

import psycopg2
from django.core.management.base import BaseCommand
from django.conf import settings

from surveys import models

DB_CONN = 'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}'
DB_CONN_STR = DB_CONN.format(**settings.DATABASES['default'])

CENSUS_AREAS = {
    'USA': ['1'],
    'Pennsylvania': ['42'],
    'Philadelphia': ['42101']
}


class Command(BaseCommand):
    help = 'Load ACS data into the database'

    def handle(self, *args, **kwargs):
        filepath = os.path.join('data', 'final', 'acs', 'census_observations.csv')
        tablename = 'surveys_censusobservation'

        copy_st = '''
            COPY {} (fips_code, variable, fields)
            FROM STDIN DELIMITER ',' CSV HEADER
        '''.format(tablename)

        with open(filepath, 'r') as fobj:
            with psycopg2.connect(DB_CONN_STR) as conn:
                with conn.cursor() as curs:
                    try:
                        curs.execute('''
                            TRUNCATE {} RESTART IDENTITY CASCADE
                        '''.format(tablename))
                        curs.copy_expert(copy_st, fobj)
                    except psycopg2.IntegrityError as e:
                        conn.rollback()
                        raise e

        self.stdout.write(self.style.SUCCESS('Imported {}'.format(filepath)))

        created_areas = 0
        for name, fips_codes in CENSUS_AREAS.items():
            _, created = models.CensusArea.objects.get_or_create(
                name=name,
                fips_codes=fips_codes
            )
            if created:
                created_areas += 1

        self.stdout.write(
            self.style.SUCCESS('Created {} CensusAreas'.format(str(created_areas)))
        )

