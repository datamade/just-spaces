from django.db import models
from django.contrib.auth.models import AbstractUser

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

    class Meta:
        ordering = ['order']
