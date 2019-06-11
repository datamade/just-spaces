from django import forms
from django.utils.translation import ugettext_lazy as _

from fobi.base import BaseFormFieldPluginForm, get_theme

from pldp.forms import GROUPS_BASIC_CHOICES

from ...utils import choices_to_help_text

theme = get_theme(request=None, as_instance=True)


class GroupsObservationalForm(forms.Form, BaseFormFieldPluginForm):
    """GroupsObservationalForm."""

    plugin_data_fields = [
        ("label", "How many people do you see in each size group?"),
        ("name", "name"),
        ("help_text", ""),
        ("required", False),
    ]

    label = forms.CharField(label="Question text",
                            required=True,
                            help_text="Use this survey question to count the \
                            group size in the given space. Everyone within a \
                            group should be individually counted in the \
                            correct group field. Following the \
                            Public Life Data Protocol, group size data will be \
                            collected in the following categories:<br /><br />"
                            + choices_to_help_text(GROUPS_BASIC_CHOICES))

    name = forms.CharField(required=True, widget=forms.widgets.HiddenInput())

    help_text = forms.CharField(
        label=_("Help text"),
        required=False,
        widget=forms.widgets.Textarea(
            attrs={'class': theme.form_element_html_class}
        )
    )

    required = forms.BooleanField(label="Required", required=False)


GroupsObservationalFormset = forms.formset_factory(GroupsObservationalForm)
