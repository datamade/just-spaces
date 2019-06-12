from django import forms
from django.utils.translation import ugettext_lazy as _

from fobi.base import BaseFormFieldPluginForm, get_theme

theme = get_theme(request=None, as_instance=True)


class AgeInterceptForm(forms.Form, BaseFormFieldPluginForm):
    """TotalForm."""

    plugin_data_fields = [
        ("label", "How old are you?"),
        ("name", "name"),
        ("age", ""),
        ("help_text", ""),
        ("required", ""),
    ]

    label = forms.CharField(label="Question text",
                            required=True,
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
                                  help_text="Is answering this question \
                                            required to submit the survey?")
