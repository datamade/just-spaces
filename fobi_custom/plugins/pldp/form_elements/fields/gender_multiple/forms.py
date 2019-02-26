from django import forms

from fobi.base import BasePluginForm
from pldp.forms import GENDER_BASIC_CHOICES


class PLDPGenderMultipleForm(forms.Form, BasePluginForm):
    """PLDPGenderMultipleForm."""

    plugin_data_fields = [
        ("label", "How many people do you see of the specified gender?"),
        ("name", ""),
        ("gender", ""),
        ("required", False),
    ]

    label = forms.CharField(label="Label",
                            required=True,
                            help_text="Use this survey element to count the \
                            number of people of a specific gender. Change \
                            the question to match your selection from the \
                            dropdown below.")
    name = forms.CharField(label="Name",
                            required=True)
    gender = forms.ChoiceField(choices=GENDER_BASIC_CHOICES,
                            help_text="Select the gender you'd like to \
                            take a count for in this survey question.")
    required = forms.BooleanField(label="Required", required=False)
