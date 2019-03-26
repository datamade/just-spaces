import sys

from django import forms

from fobi.base import FormFieldPlugin, form_element_plugin_registry
from pldp.models import Study

from .forms import PLDPStudyForm


class PLDPStudyPlugin(FormFieldPlugin):
    """PLDPStudyPlugin."""

    uid = "pldp_study"
    name = "Study"
    form = PLDPStudyForm
    group = "Public Life Data Protocol"  # Group to which the plugin belongs to

    def get_form_field_instances(self, request=None, form_entry=None,
                                 form_element_entries=None, **kwargs):

        field_kwargs = {
            'required': self.data.required,
            'label': self.data.label,
            'widget': forms.widgets.Select(attrs={}),
            'choices': Study.objects.all().values_list('id', 'title'),
            'initial': self.data.study,
        }

        return [(self.data.name, forms.ChoiceField, field_kwargs)]


form_element_plugin_registry.register(PLDPStudyPlugin)
