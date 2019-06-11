from django import forms
from django.utils.translation import ugettext_lazy as _

from fobi.base import BaseFormFieldPluginForm, get_theme
from pldp.forms import MODE_TYPE_CHOICES, MODE_BASIC_CHOICES, \
                       MODE_DETAILED_CHOICES

from ...utils import choices_to_help_text

theme = get_theme(request=None, as_instance=True)


class ModeObservationalForm(forms.Form, BaseFormFieldPluginForm):
    """ModeObservationalForm."""

    plugin_data_fields = [
        ("label", "How many people do you see using each primary mode of movement?"),
        ("name", "name"),
        ("detail_level", ""),
        ("help_text", ""),
        ("required", False),
    ]

    label = forms.CharField(label="Question text",
                            required=True,
                            help_text="Use this survey question to count the \
                            primary modes of movement for a group of people.")

    name = forms.CharField(required=True, widget=forms.widgets.HiddenInput())

    detail_level = forms.ChoiceField(choices=MODE_TYPE_CHOICES,
                                     help_text="Following the Public Life Data "
                                     "Protocol, mode data should be collected at "
                                     "one of the following levels of detail:<br />"
                                     "<br /><b>Basic</b><br />"
                                     + choices_to_help_text(MODE_BASIC_CHOICES)
                                     + "<br /><b>Detailed</b><br />"
                                     + choices_to_help_text(MODE_DETAILED_CHOICES))

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


ModeObservationalFormset = forms.formset_factory(ModeObservationalForm)
