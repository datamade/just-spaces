from django import forms
from django.utils.translation import ugettext_lazy as _

from fobi.base import BaseFormFieldPluginForm, get_theme

from ...utils import choices_to_help_text
from pldp.forms import GENDER_BASIC_CHOICES

theme = get_theme(request=None, as_instance=True)


class GenderObservationalForm(forms.Form, BaseFormFieldPluginForm):
    """GenderObservationalForm."""

    plugin_data_fields = [
        ("label", "How many people do you see of each gender?"),
        ("name", "name"),
        ("help_text", ""),
        ("required", False),
    ]

    label = forms.CharField(label="Question text",
                            required=True,
                            help_text="Use this survey question to gather data "
                            "on the perceived genders of people in a given "
                            "space. Following the Public Life Data "
                            "Protocol, gender data is collected in the "
                            "following categories:<br /><br />"
                            + choices_to_help_text(GENDER_BASIC_CHOICES))

    name = forms.CharField(required=True, widget=forms.widgets.HiddenInput())

    help_text = forms.CharField(label=_("Help text"),
                                required=False,
                                widget=forms.widgets.Textarea(
                                attrs={'class': theme.form_element_html_class}),
                                help_text="This text will show up under the \
                                          question and provide the \
                                          survey taker with additional \
                                          information."
                                )

    required = forms.BooleanField(label="Required",
                                  required=False,
                                  help_text="Is answering this question required to submit the survey?")


GenderObservationalFormset = forms.formset_factory(GenderObservationalForm)
