from django.db import models
from django.contrib.auth.models import AbstractUser

from pldp.models import Agency, Study, Location
from fobi.models import FormEntry, FormElementEntry


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

    source = models.ForeignKey(
        FormElementEntry,
        on_delete=models.CASCADE,
        null=True
    )

    class Meta:
        ordering = ['order']
