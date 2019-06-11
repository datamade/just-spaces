from django import forms
from django.utils.translation import ugettext_lazy as _

from fobi.base import BaseFormFieldPluginForm, get_theme
from pldp.forms import SURVEY_REPRESENTATION_CHOICES


theme = get_theme(request=None, as_instance=True)


class PLDPSurveyRepresentationForm(forms.Form, BaseFormFieldPluginForm):
    """PLDPSurveyRepresentationForm."""

    plugin_data_fields = [
        ("label", "Is the representation of this survey absolute or relative?"),
        ("name", "name"),
        ("default", ""),
        ("help_text", ""),
        ("required", True),
    ]

    label = forms.CharField(label="Question text",
                            required=True,
                            )

    name = forms.CharField(required=True, widget=forms.widgets.HiddenInput())

    default = forms.ChoiceField(choices=SURVEY_REPRESENTATION_CHOICES,
                                help_text="Indicate whether the data collected "
                                "is a total of the people present within the "
                                "survey count time (absolute) or a representative "
                                "sample (relative). "
                                "This will be the default, but users will be "
                                "able to change this selection when running "
                                "the survey.",
                                widget=forms.widgets.Select(
                                    attrs={'class': theme.form_element_html_class}
                                ))

    help_text = forms.CharField(
        label=_("Help text"),
        required=False,
        widget=forms.widgets.Textarea(
            attrs={'class': theme.form_element_html_class}
        )
    )

    required = forms.BooleanField(label="Required", required=False)
