from django.db import models
from django.contrib.auth.models import AbstractUser

from pldp.models import Agency, Study, Location
from fobi.models import FormEntry


class SurveyForm(FormEntry):
    published = models.BooleanField(default=False)
    study = models.ForeignKey(Study, null=True, blank=True, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, null=True, blank=True, on_delete=models.CASCADE)


class SurveyFormIntercept(SurveyForm):
    pass


class SurveyFormObservational(SurveyForm):
    pass
