from django import forms

from fobi.base import BasePluginForm
from pldp.forms import GENDER_TYPE_CHOICES


class PLDPGenderSingleForm(forms.Form, BasePluginForm):
    """PLDPGenderSingleForm."""

    plugin_data_fields = [
        ("label", ""),
        ("name", "name"),
        ("required", False),
        ("detail_level", "basic")
    ]

    label = forms.CharField(label="Label", required=True)

    name = forms.CharField(required=True, widget=forms.widgets.HiddenInput())

    required = forms.BooleanField(label="Required", required=False)
    
    detail_level = forms.ChoiceField(choices=GENDER_TYPE_CHOICES,
                                     help_text="The Public Life Data Protocol "
                                     "suggests these categories of gender: "
                                     "<br /><br />"
                                     "<b>Basic</b><br />"
                                     "Male<br />"
                                     "Female<br />"
                                     "Unknown<br />")
