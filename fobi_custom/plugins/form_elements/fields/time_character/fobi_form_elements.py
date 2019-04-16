from django import forms

from fobi.base import FormFieldPlugin, form_element_plugin_registry
from pldp.forms import SURVEY_TIME_CHARACTER_CHOICES

from .forms import TimeCharacterForm


class TimeCharacterPlugin(FormFieldPlugin):
    """TimeCharacterPlugin."""

    uid = "time_character"
    name = "Time Character"
    form = TimeCharacterForm
    group = "Public Life Data Protocol"  # Group to which the plugin belongs to

    def get_form_field_instances(self, request=None, form_entry=None,
                                 form_element_entries=None, **kwargs):

        field_kwargs = {
            'required': self.data.required,
            'label': self.data.label,
            'widget': forms.widgets.Select(attrs={}),
            'choices': SURVEY_TIME_CHARACTER_CHOICES,
            'initial': self.data.default,
        }

        return [(self.data.name, forms.ChoiceField, field_kwargs)]


form_element_plugin_registry.register(TimeCharacterPlugin)
