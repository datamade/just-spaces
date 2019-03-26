from django import forms
from django.utils.translation import ugettext_lazy as _

from fobi.base import BaseFormFieldPluginForm, get_theme
from pldp.models import Study


theme = get_theme(request=None, as_instance=True)

class PLDPStudyForm(forms.Form, BaseFormFieldPluginForm):
    """PLDPStudyForm."""

    plugin_data_fields = [
        ("label", "To which study does this survey belong?"),
        ("name", "name"),
        ("study", ""),
        ("help_text", ""),
        ("required", False),
    ]

    label = forms.CharField(label="Label",
                            required=True,
                            )

    name = forms.CharField(required=True, widget=forms.widgets.HiddenInput())

    study = forms.ChoiceField(choices=[],
                              help_text="Select the study to which this "
                              "survey belongs. This will be the default, "
                              "but users will be able to change this "
                              "selection when running the survey.",
                              widget=forms.widgets.Select(
                                attrs={'class': theme.form_element_html_class}
                              ))

    help_text = forms.CharField(
        label=_("Help text"),
        required=False,
        widget=forms.widgets.Textarea(
            attrs={'class': theme.form_element_html_class}
        )
    )

    required = forms.BooleanField(label="Required", required=False)

    def __init__(self, *args, **kwargs):
        super(PLDPStudyForm, self).__init__(*args, **kwargs)
        self.fields['study'].choices = Study.objects.all().values_list('id', 'title')
