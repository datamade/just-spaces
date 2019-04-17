from django import forms

from fobi.base import FormFieldPlugin, form_element_plugin_registry
from pldp.forms import SURVEY_MICROCLIMATE_CHOICES

from .forms import MicroclimateForm


class MicroclimatePlugin(FormFieldPlugin):
    """MicroclimatePlugin."""

    uid = "microclimate"
    name = "Microclimate"
    form = MicroclimateForm
    group = "Public Life Data Protocol"  # Group to which the plugin belongs to

    def get_form_field_instances(self, request=None, form_entry=None,
                                 form_element_entries=None, **kwargs):

        field_kwargs = {
            'required': self.data.required,
            'label': self.data.label,
            'widget': forms.widgets.Select(attrs={}),
            'choices': SURVEY_MICROCLIMATE_CHOICES,
            'initial': self.data.default,
        }

        return [(self.data.name, forms.ChoiceField, field_kwargs)]


form_element_plugin_registry.register(MicroclimatePlugin)
