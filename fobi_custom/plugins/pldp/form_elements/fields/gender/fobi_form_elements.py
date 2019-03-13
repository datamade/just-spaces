import sys

from django import forms

from fobi.base import FormFieldPlugin, form_element_plugin_registry

from .forms import PLDPGenderForm
from pldp.forms import GENDER_BASIC_CHOICES


class PLDPGenderPlugin(FormFieldPlugin):
    """PLDPGenderPlugin."""

    uid = "pldp_gender"
    name = "Gender"
    form = PLDPGenderForm
    group = "Public Life Data Protocol"  # Group to which the plugin belongs to

    def get_form_field_instances(self, request=None, form_entry=None,
                                 form_element_entries=None, **kwargs):

        field_kwargs = {
            'label': self.data.label,
            'help_text': self.data.help_text,
            'required': self.data.required,
            'widget': forms.widgets.NumberInput(attrs={}),
        }

        return [(self.data.name, forms.IntegerField, field_kwargs)]


form_element_plugin_registry.register(PLDPGenderPlugin)
