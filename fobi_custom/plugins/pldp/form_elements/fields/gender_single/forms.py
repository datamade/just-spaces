from django import forms
from django.utils.translation import ugettext_lazy as _

from fobi.base import BaseFormFieldPluginForm, get_theme
from pldp.forms import GENDER_TYPE_CHOICES

theme = get_theme(request=None, as_instance=True)


class PLDPGenderSingleForm(forms.Form, BaseFormFieldPluginForm):
    """PLDPGenderSingleForm."""

    plugin_data_fields = [
        ("label", ""),
        ("name", "name"),
        ("detail_level", "basic"),
        ("help_text", ""),
        ("required", False),
    ]

    label = forms.CharField(label="Label", required=True)

    name = forms.CharField(required=True, widget=forms.widgets.HiddenInput())

    detail_level = forms.ChoiceField(choices=GENDER_TYPE_CHOICES,
                                     help_text="The Public Life Data Protocol "
                                     "suggests these categories of gender: "
                                     "<br /><br />"
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
