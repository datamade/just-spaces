from django import forms
from django.utils.translation import ugettext_lazy as _

from fobi.base import BaseFormFieldPluginForm, get_theme

theme = get_theme(request=None, as_instance=True)


class HouseholdTenureForm(forms.Form, BaseFormFieldPluginForm):
    """HouseholdTenureForm."""

    plugin_data_fields = [
        ("label", "What year did you move into your current address?"),
        ("name", "name"),
        ("help_text", ""),
        ("required", False),
    ]

    label = forms.CharField(label="Question text",
                            required=True,
                            help_text="This question will let users enter a number."
                            )

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
