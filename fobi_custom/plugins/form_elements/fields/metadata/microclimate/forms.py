from django import forms
from django.utils.translation import ugettext_lazy as _

from fobi.base import BaseFormFieldPluginForm, get_theme

from ...utils import choices_to_help_text
from pldp.forms import SURVEY_MICROCLIMATE_CHOICES


theme = get_theme(request=None, as_instance=True)


class MicroclimateForm(forms.Form, BaseFormFieldPluginForm):
    """MicroclimateForm."""

    plugin_data_fields = [
        ("label", "What are the current weather conditions?"),
        ("name", "name"),
        ("default", ""),
        ("help_text", ""),
        ("required", False),
    ]

    label = forms.CharField(
        label="Question text",
        required=True,
        help_text="Following categories defined by the Public Life Data Protocol, the following \
                  options will be provided: <br /><br />" +
                  choices_to_help_text(SURVEY_MICROCLIMATE_CHOICES)
        )

    name = forms.CharField(required=True, widget=forms.widgets.HiddenInput())

    default = forms.ChoiceField(label="Default answer",
                                choices=SURVEY_MICROCLIMATE_CHOICES,
                                help_text="This will be the default, but users will be "
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
        ),
        help_text="This text will show up under the \
                  question and provide the \
                  survey taker with additional \
                  information."
    )

    required = forms.BooleanField(
        label="Required",
        required=False,
        help_text="Is answering this question required to submit the survey?"
    )
