import os
import csv
import json

from django.core.management.base import BaseCommand, CommandError
from django.contrib.gis.utils import LayerMapping
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
        self.stdout.write(self.style.SUCCESS('Importing ACS data...'))

        obs_created, obs_updated = 0, 0
        filepath = os.path.join('data', 'final', 'acs', 'census_observations.csv')
        with open(filepath) as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Taken together, FIPS code and variable compromise a primary
                # key for ACS data; optionally update the object with new data
                # if it already exists according to this set of primary keys
                pk_data = {
                    'fips_code': row['fips'],
                    'variable': row['variable'],
                }
                defaults = {
                    'fields': json.loads(row['fields']),
                }
                _, created = models.CensusObservation.objects.update_or_create(
                    defaults=defaults,
                    **pk_data
                )
                if created:
                    obs_created += 1
                else:
                    obs_updated += 1

        self.stdout.write(
            self.style.SUCCESS(
                'Created {}, updated {} CensusObservations'.format(
                    obs_created,
                    obs_updated
                )
            )
        )

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

        self.stdout.write(self.style.SUCCESS('Importing CensusBlockGroups...'))

        shapefile = os.path.join('data', 'final', 'shapefiles', 'cb_2018_42_bg_500k.shp')

        try:
            assert os.path.exists(shapefile)
        except AssertionError:
            msg = ('Required shapefile {} not found. '.format(shapefile) +
                   'Run `make all` from the data directory to download it.')
            raise CommandError(msg)

        blockgroup_mapping = {
            'fips_code': 'GEOID',
            'geom': 'POLYGON',
        }

        lm = LayerMapping(
            models.CensusBlockGroup,
            shapefile,
            blockgroup_mapping,
            transform=False,
            unique='fips_code',
        )
        lm.save()

        self.stdout.write(self.style.SUCCESS('Done!'))
