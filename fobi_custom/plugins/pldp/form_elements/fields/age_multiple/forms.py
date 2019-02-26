from django import forms

from fobi.base import BasePluginForm
from pldp.forms import AGE_BASIC_CHOICES, AGE_DETAILED_CHOICES, \
                       AGE_COMPLEX_CHOICES


class PLDPAgeMultipleForm(forms.Form, BasePluginForm):
    """PLDPAgeMultipleForm."""

    plugin_data_fields = [
        ("label", "How many people do you see between the ages of 0-14?"),
        ("name", ""),
        ("age range", ""),
        ("required", False),
    ]

    structured_choices = tuple((('basic', tuple(AGE_BASIC_CHOICES)),
                   ('detailed', tuple(AGE_DETAILED_CHOICES)),
                   ('complex', tuple(AGE_COMPLEX_CHOICES))))

    label = forms.CharField(label="Label",
                            required=True,
                            help_text="Use this survey element to count the \
                            number of people of a specific age range. Change \
                            the question to match your selection from the \
                            dropdown below.")
    name = forms.CharField(label="Name",
                            required=True)
    age = forms.ChoiceField(choices=structured_choices,
                            help_text="Select the age range you'd like to \
                            take a count for in this survey question.")
    required = forms.BooleanField(label="Required", required=False)
