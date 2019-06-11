from django import forms
from django.utils.translation import ugettext_lazy as _

from fobi.base import BaseFormFieldPluginForm, get_theme
from pldp.forms import AGE_TYPE_CHOICES, AGE_BASIC_CHOICES, \
                       AGE_DETAILED_CHOICES, AGE_COMPLEX_CHOICES

from ...utils import choices_to_help_text

theme = get_theme(request=None, as_instance=True)


class AgeObservationalForm(forms.Form, BaseFormFieldPluginForm):
    """AgeObservationalForm."""

    plugin_data_fields = [
        ("label", "How many people do you see in each age range?"),
        ("name", "name"),
        ("detail_level", ""),
        ("help_text", ""),
        ("required", False),
    ]

    label = forms.CharField(label="Question text",
                            required=True,
                            help_text="Use this survey element to count the \
                            observed ages of a group of people.")

    name = forms.CharField(required=True, widget=forms.widgets.HiddenInput())

    detail_level = forms.ChoiceField(choices=AGE_TYPE_CHOICES,
                                     help_text="Following the Public Life Data "
                                     "Protocol, age data should be collected at "
                                     "one of the following levels of detail:<br />"
                                     "<br /><b>Basic</b><br />"
                                     + choices_to_help_text(AGE_BASIC_CHOICES)
                                     + "<br /><b>Detailed</b><br />"
                                     + choices_to_help_text(AGE_DETAILED_CHOICES)
                                     + "<br /><b>Complex</b><br />"
                                     + choices_to_help_text(AGE_COMPLEX_CHOICES))

    help_text = forms.CharField(
        label=_("Help text"),
        required=False,
        widget=forms.widgets.Textarea(
            attrs={'class': theme.form_element_html_class}
        )
    )

    required = forms.BooleanField(label="Required", required=False)


AgeObservationalFormset = forms.formset_factory(AgeObservationalForm)
