from django import forms

from fobi.base import FormFieldPlugin, form_element_plugin_registry
from ..forms import EMPLOYMENT_CHOICES

from .forms import EmploymentForm


class EmploymentPlugin(FormFieldPlugin):
    """EmploymentPlugin."""

    uid = "employment"
    name = "Employment"
    form = EmploymentForm
    group = "Intercept"  # Group to which the plugin belongs to

    def get_form_field_instances(self, request=None, form_entry=None,
                                 form_element_entries=None, **kwargs):

        field_kwargs = {
            'required': self.data.required,
            'label': self.data.label,
            'widget': forms.widgets.Select(attrs={}),
            'choices': EMPLOYMENT_CHOICES,
        }

        return [(self.data.name, forms.ChoiceField, field_kwargs)]


form_element_plugin_registry.register(EmploymentPlugin)
