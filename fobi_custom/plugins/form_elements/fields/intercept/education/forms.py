from django import forms
from django.utils.translation import ugettext_lazy as _

from fobi.base import BaseFormFieldPluginForm, get_theme

from ...utils import choices_to_help_text_skip_first
from ..forms import EDUCATION_CHOICES


theme = get_theme(request=None, as_instance=True)


class EducationForm(forms.Form, BaseFormFieldPluginForm):
    """EducationForm."""

    plugin_data_fields = [
        ("label", "What is your highest formal degree of education?"),
        ("name", "name"),
        ("help_text", ""),
        ("required", False),
    ]

    label = forms.CharField(
        label="Question text",
        required=True,
        help_text="Following categories defined by the Census, the following \
                  options will be provided: <br /><br />" +
                  choices_to_help_text_skip_first(EDUCATION_CHOICES)
        )

    name = forms.CharField(required=True, widget=forms.widgets.HiddenInput())

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
