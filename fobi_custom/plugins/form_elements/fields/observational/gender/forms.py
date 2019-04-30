from django import forms
from django.utils.translation import ugettext_lazy as _

from fobi.base import BaseFormFieldPluginForm, get_theme

theme = get_theme(request=None, as_instance=True)


class GenderObservationalForm(forms.Form, BaseFormFieldPluginForm):
    """GenderObservationalForm."""

    plugin_data_fields = [
        ("label", "How many people do you see of each gender?"),
        ("name", "name"),
        ("help_text", ""),
        ("required", False),
    ]

    label = forms.CharField(label="Label",
                            required=True,
                            help_text="Use this survey element to count the \
                            observed genders of a group of people. Options are \
                            male, female, and unknown.")

    name = forms.CharField(required=True, widget=forms.widgets.HiddenInput())


    help_text = forms.CharField(
        label=_("Help text"),
        required=False,
        widget=forms.widgets.Textarea(
            attrs={'class': theme.form_element_html_class}
        )
    )

    required = forms.BooleanField(label="Required", required=False)


GenderObservationalFormset = forms.formset_factory(GenderObservationalForm)
