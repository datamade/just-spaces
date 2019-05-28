from django.db import models
from django.contrib.postgres import fields as pg_fields
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import JSONField

from pldp.models import Agency, Study, Location
from fobi.models import FormEntry


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


class CensusObservation(models.Model):
    fips_code = models.CharField(max_length=255)
    variable = models.CharField(max_length=255)
    fields = JSONField()


class CensusArea(models.Model):
    name = models.CharField(max_length=255)
    fips_codes = pg_fields.ArrayField(models.CharField(max_length=12))

    def __str__(self):
        return self.name

    def get_observation_data(self, variable):
        """
        Given an ACS variable, return the observation data for this area.

        :param variable: The ACS variable in question.
        :returns: A dictionary representing the stored data of the CensusObservation
                  objects for the given area and variable.
        """
        observations = CensusObservation.objects.filter(
            variable=variable,
            fips_code__in=self.fips_codes
        )
        return {observation.fips_code: observation.fields for observation in observations}


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

    census_areas = models.ManyToManyField(CensusArea)

    class Meta:
        ordering = ['order']
