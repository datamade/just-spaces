import os
import csv
import json

from django.core.management.base import BaseCommand, CommandError
from django.contrib.gis.utils import LayerMapping
from django.contrib.gis.geos import Point
from django.conf import settings
from django.db import transaction
from django.utils.text import slugify

from surveys import models
from data.scripts.states import STATES, REGIONS, COUNTY_TO_REGION

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


class BlockgroupLayerMapping(LayerMapping):
    """
    Custom GeoDjango LayerMapping allowing us to assign Regions to Blockgroups.
    """
    def feature_kwargs(self, feature):
        kwargs = super().feature_kwargs(feature)
        county_fips = feature.get('STATEFP') + feature.get('COUNTYFP')
        region_slug = slugify(COUNTY_TO_REGION[county_fips])
        kwargs.update({'region': models.CensusRegion.objects.get(slug=region_slug)})
        return kwargs


class Command(BaseCommand):
    help = 'Load ACS data into the database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--observations-only',
            action='store_true',
            default=False,
            help="Only import CensusObservations"
        )
        parser.add_argument(
            '--regions-only',
            action='store_true',
            default=False,
            help="Only import CensusRegions"
        )
        parser.add_argument(
            '--areas-only',
            action='store_true',
            default=False,
            help="Only import CensusAreas"
        )
        parser.add_argument(
            '--blockgroups-only',
            action='store_true',
            default=False,
            help="Only import CensusBlockgroups"
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Importing data...'))

        if options['observations_only']:
            self.import_observations()
        elif options['regions_only']:
            self.import_regions()
        elif options['areas_only']:
            self.import_areas()
        elif options['blockgroups_only']:
            self.import_blockgroups()
        else:
            self.import_all()

    def import_all(self):
        self.import_observations()
        self.import_regions()
        self.import_areas()
        self.import_blockgroups()

    def import_observations(self):
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

    def import_regions(self):
        regions_created, regions_updated = 0, 0
        for name, region_vars in REGIONS.items():
            pk_data = {'name': name, 'slug': slugify(name)}
            defaults = {
                'fips_codes': region_vars['counties'],
                'centroid': Point(region_vars['centroid']),
                'default_zoom': region_vars['default_zoom'],
            }
            _, created = models.CensusRegion.objects.update_or_create(
                defaults=defaults,
                **pk_data
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

    def import_areas(self):
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

    def import_blockgroups(self):
        shapefile_filenames = ['cb_2018_{}_bg_500k.shp'.format(fips)
                               for fips in STATES.keys()]
        shapefiles = [os.path.join('data', 'final', 'shapefiles', fname)
                      for fname in shapefile_filenames]

        with transaction.atomic():
            # Truncate table, because otherwise LayerMapping will incorrectly
            # attempt to update the layer and mess up its geometry
            # See: https://stackoverflow.com/q/30300876
            models.CensusBlockGroup.objects.all().delete()
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
                lm = BlockgroupLayerMapping(
                    model=models.CensusBlockGroup,
                    data=shapefile,
                    mapping=blockgroup_mapping,
                    transform=False,
                    unique='fips_code',
                )
                lm.save(progress=True, strict=True)

        self.stdout.write(self.style.SUCCESS('Imported CensusBlockgroups'))
