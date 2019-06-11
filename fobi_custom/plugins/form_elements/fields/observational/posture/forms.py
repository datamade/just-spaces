from django import forms
from django.utils.translation import ugettext_lazy as _

from fobi.base import BaseFormFieldPluginForm, get_theme
from pldp.forms import POSTURE_TYPE_CHOICES, POSTURE_BASIC_CHOICES, \
                       POSTURE_DETAILED_CHOICES

from ...utils import choices_to_help_text

theme = get_theme(request=None, as_instance=True)


class PostureObservationalForm(forms.Form, BaseFormFieldPluginForm):
    """PostureObservationalForm."""

    plugin_data_fields = [
        ("label", "How many people do you see in each posture?"),
        ("name", "name"),
        ("detail_level", ""),
        ("help_text", ""),
        ("required", False),
    ]

    label = forms.CharField(label="Question text",
                            required=True,
                            help_text="Use this survey question to count the \
                            primary postures of a group of people.")

    name = forms.CharField(required=True, widget=forms.widgets.HiddenInput())

    detail_level = forms.ChoiceField(choices=POSTURE_TYPE_CHOICES,
                                     help_text="Following the Public Life Data "
                                     "Protocol, posture data should be collected at "
                                     "one of the following levels of detail:<br />"
                                     "<br /><b>Basic</b><br />"
                                     + choices_to_help_text(POSTURE_BASIC_CHOICES)
                                     + "<br /><b>Detailed</b><br />"
                                     + choices_to_help_text(POSTURE_DETAILED_CHOICES))

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
                                  

PostureObservationalFormset = forms.formset_factory(PostureObservationalForm)
