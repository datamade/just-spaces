from django import forms

from fobi.base import FormFieldPlugin, form_element_plugin_registry
from pldp.forms import SURVEY_METHOD_CHOICES

from .forms import PLDPSurveyMethodForm


class PLDPSurveyMethodPlugin(FormFieldPlugin):
    """PLDPSurveyMethodPlugin."""

    uid = "method"
    name = "Survey Method"
    form = PLDPSurveyMethodForm
    group = "Survey Metadata"  # Group to which the plugin belongs to

    def get_form_field_instances(self, request=None, form_entry=None,
                                 form_element_entries=None, **kwargs):

        field_kwargs = {
            'required': self.data.required,
            'label': self.data.label,
            'widget': forms.widgets.Select(attrs={}),
            'choices': SURVEY_METHOD_CHOICES,
            'initial': self.data.default,
        }

        return [(self.data.name, forms.ChoiceField, field_kwargs)]


form_element_plugin_registry.register(PLDPSurveyMethodPlugin)
