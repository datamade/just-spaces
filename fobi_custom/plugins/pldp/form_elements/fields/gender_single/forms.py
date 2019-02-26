from django import forms

from fobi.base import BasePluginForm
from pldp.forms import GENDER_TYPE_CHOICES


class PLDPGenderSingleForm(forms.Form, BasePluginForm):
    """PLDPGenderSingleForm."""

    plugin_data_fields = [
        ("label", ""),
        ("name", ""),
        ("required", False),
        ("detail_level", "basic")
    ]

    label = forms.CharField(label="Label", required=True)
    name = forms.CharField(label="Name", required=True)
    required = forms.BooleanField(label="Required", required=False)
    detail_level = forms.ChoiceField(choices=GENDER_TYPE_CHOICES)
