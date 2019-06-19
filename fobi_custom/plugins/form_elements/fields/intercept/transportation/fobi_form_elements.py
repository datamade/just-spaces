from django import forms

from fobi.base import FormFieldPlugin, form_element_plugin_registry
from ..forms import TRANSPORTATION_CHOICES

from .forms import TransportationForm


class TransportationPlugin(FormFieldPlugin):
    """TransportationPlugin."""

    uid = "transportation"
    name = "How did you travel here?"
    form = TransportationForm
    group = "Intercept"  # Group to which the plugin belongs to

    def get_form_field_instances(self, request=None, form_entry=None,
                                 form_element_entries=None, **kwargs):

        field_kwargs = {
            'required': self.data.required,
            'label': self.data.label,
            'widget': forms.widgets.RadioSelect(attrs={}),
            'choices': TRANSPORTATION_CHOICES,
        }

        return [(self.data.name, forms.ChoiceField, field_kwargs)]


form_element_plugin_registry.register(TransportationPlugin)
