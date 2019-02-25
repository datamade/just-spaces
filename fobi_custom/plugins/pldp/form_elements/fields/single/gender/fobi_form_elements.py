import sys

from django import forms

from fobi.base import FormFieldPlugin, form_element_plugin_registry

from .forms import PLDPGenderSingleForm
from pldp.forms import *


class PLDPGenderSinglePlugin(FormFieldPlugin):
    """PLDPGenderSinglePlugin."""

    uid = "pldp_gender_single"
    name = "Gender (single)"
    form = PLDPGenderSingleForm
    group = "Public Life Data Protocol"  # Group to which the plugin belongs to

    def get_form_field_instances(self, request=None, form_entry=None,
                                 form_element_entries=None, **kwargs):

        choice_level = 'GENDER_{}_CHOICES'.format(self.data.detail_level.upper())
        choices = getattr(sys.modules[__name__], choice_level)

        print(choices)

        field_kwargs = {
            'required': self.data.required,
            'label': self.data.label,
            'widget': forms.widgets.Select(attrs={}),
            'choices': choices,
        }

        return [(self.data.name, forms.ChoiceField, field_kwargs)]


form_element_plugin_registry.register(PLDPGenderSinglePlugin)
