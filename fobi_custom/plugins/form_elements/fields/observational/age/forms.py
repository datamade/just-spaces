from django import forms
from django.utils.translation import ugettext_lazy as _

from fobi.base import BaseFormFieldPluginForm, get_theme
from pldp.forms import AGE_TYPE_CHOICES

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

    label = forms.CharField(label="Label",
                            required=True,
                            help_text="Use this survey element to count the \
                            observed ages of a group of people.")

    name = forms.CharField(required=True, widget=forms.widgets.HiddenInput())

    detail_level = forms.ChoiceField(choices=AGE_TYPE_CHOICES,
                                     help_text="Following the Public Life Data "
                                     "Protocol, age data should be collected at "
                                     "one of the following levels of detail:<br /><br />"
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


AgeObservationalFormset = forms.formset_factory(AgeObservationalForm)