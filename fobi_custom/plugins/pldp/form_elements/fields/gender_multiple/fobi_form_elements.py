import sys

from django import forms

from fobi.base import FormFieldPlugin, form_element_plugin_registry

from .forms import PLDPGenderMultipleForm
from pldp.forms import GENDER_BASIC_CHOICES


class PLDPGenderMultiplePlugin(FormFieldPlugin):
    """PLDPGenderMultiplePlugin."""

    uid = "pldp_gender_multiple"
    name = "Gender, multiple"
    form = PLDPGenderMultipleForm
    group = "Public Life Data Protocol"  # Group to which the plugin belongs to

    def get_form_field_instances(self, request=None, form_entry=None,
                                 form_element_entries=None, **kwargs):

        field_kwargs = {
            'label': self.data.label,
            'gender': self.data.gender,
            'help_text': self.data.help_text,
            'required': self.data.required,
            'widget': forms.widgets.NumberInput(attrs={}),
        }

        return [(self.data.name, forms.IntegerField, field_kwargs)]


form_element_plugin_registry.register(PLDPGenderMultiplePlugin)
