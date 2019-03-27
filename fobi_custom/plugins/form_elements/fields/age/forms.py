from django import forms
from django.utils.translation import ugettext_lazy as _

from fobi.base import BaseFormFieldPluginForm, get_theme
from pldp.forms import AGE_BASIC_CHOICES, AGE_DETAILED_CHOICES, \
                       AGE_COMPLEX_CHOICES

theme = get_theme(request=None, as_instance=True)

class PLDPAgeForm(forms.Form, BaseFormFieldPluginForm):
    """PLDPAgeForm."""

    plugin_data_fields = [
        ("label", "How many people do you see between the ages of 0-14?"),
        ("name", "name"),
        ("age", ""),
        ("help_text", ""),
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

    name = forms.CharField(required=True, widget=forms.widgets.HiddenInput())

    age = forms.ChoiceField(choices=structured_choices,
                            help_text="Select the age range you'd like to "
                            "take a count for in this survey question. "
                            "The Public Life Data Protocol "
                            "suggests collecting age data at one "
                            "of three levels of detail:<br /><br />"
                            "<b>Basic</b><br />"
                            "0-14<br />"
                            "15-24<br />"
                            "25-64<br />"
                            "65+<br /><br />"
                            "<b>Detailed</b><br />"
                            "0-4<br />"
                            "5-14<br />"
                            "15-24<br />"
                            "25-44<br />"
                            "45-64<br />"
                            "65-74<br />"
                            "75+<br /><br />"
                            "<b>Complex</b><br />"
                            "0-4<br />"
                            "5-9<br />"
                            "10-14<br />"
                            "15-17<br />"
                            "18-24<br />"
                            "25-34<br />"
                            "35-44<br />"
                            "45-54<br />"
                            "55-64<br />"
                            "65-74<br />"
                            "75+<br /><br />")

    help_text = forms.CharField(
        label=_("Help text"),
        required=False,
        widget=forms.widgets.Textarea(
            attrs={'class': theme.form_element_html_class}
        )
    )

    required = forms.BooleanField(label="Required", required=False)
