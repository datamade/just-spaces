from django import forms
from django.utils.translation import ugettext_lazy as _

from fobi.base import BaseFormFieldPluginForm, get_theme
from pldp.forms import MODE_TYPE_CHOICES, MODE_BASIC_CHOICES, \
                       MODE_DETAILED_CHOICES, AGE_BASIC_CHOICES, AGE_COMPLEX_CHOICES, AGE_DETAILED_CHOICES

from ...utils import choices_to_help_text

theme = get_theme(request=None, as_instance=True)


class ModeObservationalForm(forms.Form, BaseFormFieldPluginForm):
    """ModeObservationalForm."""

    plugin_data_fields = [
        ("label", "How many people do you see using each primary mode of movement?"),
        ("name", "name"),
        ("categories", ""),
        ("help_text", ""),
        ("required", False),
    ]

    label = forms.CharField(
        label="Label",
        required=True,
        help_text="Use this survey question to count the \
        primary modes of movement for a group of people."
    )

    name = forms.CharField(required=True, widget=forms.widgets.HiddenInput())

    categories = forms.MultipleChoiceField(
        choices=MODE_BASIC_CHOICES,
        widget=forms.widgets.CheckboxSelectMultiple(),
    )

    help_text = forms.CharField(
        label=_("Help text"),
        required=False,
        widget=forms.widgets.Textarea(
            attrs={'class': theme.form_element_html_class}
        )
    )

    required = forms.BooleanField(label="Required", required=False)

    def clean_categories(self):
        selected_categories = []
        for value, display_value in MODE_BASIC_CHOICES:
            if value in self.cleaned_data['categories']:
                selected_categories += [(value, display_value)]

        print(selected_categories)
        return selected_categories


ModeObservationalFormset = forms.formset_factory(ModeObservationalForm)
