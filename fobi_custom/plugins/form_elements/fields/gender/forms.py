from django import forms
from django.utils.translation import ugettext_lazy as _

from fobi.base import BaseFormFieldPluginForm, get_theme
from pldp.forms import GENDER_BASIC_CHOICES

theme = get_theme(request=None, as_instance=True)


class PLDPGenderForm(forms.Form, BaseFormFieldPluginForm):
    """PLDPGenderForm."""

    plugin_data_fields = [
        ("label", "How many people do you see of the following gender? Men"),
        ("name", "name"),
        ("gender", ""),
        ("help_text", ""),
        ("required", False),
    ]

    label = forms.CharField(label="Label",
                            required=True,
                            help_text="Use this survey element to count the "
                            "number of people of a specific gender. Change "
                            "the question to match your selection from the "
                            "dropdown below.")

    name = forms.CharField(required=True, widget=forms.widgets.HiddenInput())

    gender = forms.ChoiceField(choices=GENDER_BASIC_CHOICES,
                            help_text="Select the gender you'd like to "
                            "take a count for in this survey question. "
                            "The Public Life Data Protocol suggests these "
                            "categories of gender: <br /><br />"
                            "<b>Basic</b><br />"
                            "Male<br />"
                            "Female<br />"
                            "Unknown<br />")

    help_text = forms.CharField(
        label=_("Help text"),
        required=False,
        widget=forms.widgets.Textarea(
            attrs={'class': theme.form_element_html_class}
        )
    )

    required = forms.BooleanField(label="Required", required=False)
