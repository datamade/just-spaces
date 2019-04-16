from django import forms

from fobi.base import FormFieldPlugin, form_element_plugin_registry
from pldp.forms import SURVEY_REPRESENTATION_CHOICES

from .forms import PLDPSurveyRepresentationForm


class PLDPSurveyRepresentationPlugin(FormFieldPlugin):
    """PLDPSurveyRepresentationPlugin."""

    uid = "survey_representation"
    name = "Survey Representation"
    form = PLDPSurveyRepresentationForm
    group = "Public Life Data Protocol"  # Group to which the plugin belongs to

    def get_form_field_instances(self, request=None, form_entry=None,
                                 form_element_entries=None, **kwargs):

        field_kwargs = {
            'required': self.data.required,
            'label': self.data.label,
            'widget': forms.widgets.Select(attrs={}),
            'choices': SURVEY_REPRESENTATION_CHOICES,
            'initial': self.data.default,
        }

        return [(self.data.name, forms.ChoiceField, field_kwargs)]


form_element_plugin_registry.register(PLDPSurveyRepresentationPlugin)
