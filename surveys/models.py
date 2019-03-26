from django.db import models
from django.contrib.auth.models import AbstractUser

from pldp.models import Agency

class JustSpacesUser(AbstractUser):
    agency = models.ForeignKey(Agency, null=True, blank=True, on_delete=models.CASCADE)
