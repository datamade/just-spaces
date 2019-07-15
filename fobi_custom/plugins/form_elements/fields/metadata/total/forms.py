from django import forms
from django.utils.translation import ugettext_lazy as _

from fobi.base import BaseFormFieldPluginForm, get_theme

theme = get_theme(request=None, as_instance=True)


class TotalForm(forms.Form, BaseFormFieldPluginForm):
    """TotalForm."""

    plugin_data_fields = [
        ("label", "What is the total number of people counted in this survey?"),
        ("name", "name"),
        ("help_text", ""),
        ("required", True),
    ]

    label = forms.CharField(label="Question text",
                            required=True,
                            help_text="Use this survey element to count the \
                            total number of people. This is a required "
                            "field on observational surveys.")

    name = forms.CharField(required=True, widget=forms.widgets.HiddenInput())

    help_text = forms.CharField(label=_("Help text"),
                                required=False,
                                widget=forms.widgets.Textarea(
                                attrs={'class': theme.form_element_html_class})
                                )

    required = forms.BooleanField(label="Required",
                                  required=False,
                                  widget=forms.widgets.HiddenInput())
