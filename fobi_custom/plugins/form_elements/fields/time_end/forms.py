from django import forms
from django.utils.translation import ugettext_lazy as _

from fobi.base import BaseFormFieldPluginForm, get_theme

theme = get_theme(request=None, as_instance=True)


class TimeStopForm(forms.Form, BaseFormFieldPluginForm):
    """TimeStopForm."""

    plugin_data_fields = [
        ("label", "What is the stop time of this survey?"),
        ("name", "name"),
        ("age", ""),
        ("help_text", ""),
        ("required", False),
    ]

    label = forms.CharField(label="Label",
                            required=True,
                            help_text="If this question is left blank or "
                            "not included, end time will be recorded as "
                            "the time the survey is submitted.")

    name = forms.CharField(required=True, widget=forms.widgets.HiddenInput())

    help_text = forms.CharField(label=_("Help text"),
                                required=False,
                                widget=forms.widgets.Textarea(
                                attrs={'class': theme.form_element_html_class})
                                )

    required = forms.BooleanField(label="Required",
                                  required=False)
