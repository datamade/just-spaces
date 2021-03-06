from django.db import models
from django.contrib.gis.db import models as geo_models
from django.contrib.gis.geos import Point
from django.contrib.postgres import fields as pg_fields
from django.contrib.postgres.fields import JSONField

from pldp.models import Study, Location, SurveyComponent, Agency
from fobi.models import FormEntry

from fobi_custom.plugins.form_elements.fields import types as fobi_types


class SurveyFormEntry(FormEntry):
    SURVEY_TYPE_CHOICES = (
        ('intercept', 'Intercept'),
        ('observational', 'Observational'),
    )

    published = models.BooleanField(
        default=False
    )

    study = models.ForeignKey(
        Study,
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )

    location = models.ForeignKey(
        Location,
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )

    type = models.CharField(
        max_length=50,
        choices=SURVEY_TYPE_CHOICES,
        default='intercept'
    )

    survey_template = models.ForeignKey(
        FormEntry,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="survey_template_name"
    )

    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class CensusRegion(models.Model):
    # FIPS Codes that define this region, typically a set of Counties
    fips_codes = pg_fields.ArrayField(models.CharField(max_length=12))
    slug = models.SlugField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    centroid = geo_models.PointField(default=Point(40, -75.16))
    default_zoom = models.PositiveIntegerField(default=11)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class CensusBlockGroup(models.Model):
    region = models.ForeignKey('CensusRegion', on_delete=models.PROTECT)
    fips_code = models.CharField(max_length=12, primary_key=True)
    geom = geo_models.MultiPolygonField(srid=4269)


class CensusObservation(models.Model):
    fips_code = models.CharField(max_length=255)
    variable = models.CharField(max_length=255)
    fields = JSONField()

    class Meta:
        unique_together = ['fips_code', 'variable']


class CensusArea(models.Model):
    name = models.CharField(max_length=255)
    fips_codes = pg_fields.ArrayField(
        models.CharField(max_length=12),
        verbose_name='Block Groups',
        help_text=(
            'Select one or more Census block groups that comprise this area. '
            'Add or remove a block group by clicking on it, or remove all block '
            'groups by clicking the "Clear all" button.'
        )
    )
    agency = models.ForeignKey(
        Agency,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        default=None,
        help_text=(
            'Select the agency that should be able to view and edit this area. '
            'Leave this box blank if you would like this area to be available to '
            'all agencies.'
        )
    )
    region = models.ForeignKey('CensusRegion', on_delete=models.PROTECT)
    is_active = models.BooleanField(default=True)
    is_preset = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def get_observations_from_component(self, component_name):
        """
        Given the name of a SurveyComponent, return the ACS observation data for this area.

        :param component_name: The name of a SurveyComponent
        :returns: A dictionary representing the stored data of the CensusObservation
                  objects for the given area and SurveyComponent
        """
        component = SurveyComponent.objects.filter(name=component_name).first()
        if component:
            variable = fobi_types.TYPES_TO_ACS_VARIABLES.get(component.type)
            if variable:
                detailed_variable = variable.get(component.detail_level)
                observations = CensusObservation.objects.filter(
                    variable=detailed_variable,
                    fips_code__in=self.fips_codes
                )
                if len(observations) > 0:
                    categories = list(observations[0].fields.keys())
                    return {category: sum(observation.fields[category] for observation in observations)
                            for category in categories}
                else:
                    return {}
            else:
                raise CensusObservation.DoesNotExist(
                    'No corresponding ACS variable for Fobi type: {}'.format(
                        component.type
                    )
                )
        else:
            raise CensusObservation.DoesNotExist(
                'No SurveyComponent found with the name: {}'.format(component_name)
            )


class SurveyChart(models.Model):

    form_entry = models.ForeignKey(
        SurveyFormEntry,
        on_delete=models.CASCADE
    )

    order = models.IntegerField(default=0)

    short_description = models.TextField(blank=True)

    # A foreign key to the 'name' field on SurveyComponents, which uniquely
    # identifies which FormElementEntry the SurveyComponent is a part of
    primary_source = models.CharField(
        max_length=500,
        blank=True,
        null=True
    )

    census_areas = models.ManyToManyField(CensusArea, blank=True)

    class Meta:
        ordering = ['order']
