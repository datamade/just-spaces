import os
import csv
import json

from django.core.management.base import BaseCommand, CommandError
from django.contrib.gis.utils import LayerMapping
from django.conf import settings
from django.utils import slugify

from surveys import models
from data.scripts.states import STATES, REGIONS

DB_CONN = 'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}'
DB_CONN_STR = DB_CONN.format(**settings.DATABASES['default'])

PRESET_AREAS = {
    'USA': {
        'region': 'philadelphia',  # Bogus region, since this Area is preset
        'fips_codes': ['1'],
    },
    'Pennsylvania': {
        'region': 'philadelphia',  # Bogus region
        'fips_codes': ['42'],
    },
    'Philadelphia': {
        'region': 'philadelphia',
        'fips_codes': ['42101']
    }
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

        regions_created, regions_updated = 0, 0
        for name, fips_codes in REGIONS.items():
            _, created = models.CensusRegion.objects.get_or_create(
                fips_codes=fips_codes,
                name=name,
                slug=slugify(name)
            )
            if created:
                regions_created += 1
            else:
                regions_updated += 1

        self.stdout.write(
            self.style.SUCCESS(
                'Created {}, updated {} CensusRegions'.format(
                    regions_created,
                    regions_updated
                )
            )
        )

        areas_created, areas_updated = 0, 0
        for name, variables in PRESET_AREAS.items():
            _, created = models.CensusArea.objects.get_or_create(
                name=name,
                fips_codes=variables['fips_codes'],
                region=variables['region'],
                is_preset=True
            )
            if created:
                areas_created += 1
            else:
                areas_updated += 1

        self.stdout.write(
            self.style.SUCCESS(
                'Created {}, updated {} CensusAreas'.format(
                    areas_created,
                    areas_updated
                )
            )
        )

        shapefile_filenames = ['cb_2018_{}_bg_500k'.format(fips) for fips in STATES.keys()]
        shapefiles = [os.path.join('data', 'final', 'shapefiles', fname)
                      for fname in shapefile_filenames]

        for shapefile in shapefiles:
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
