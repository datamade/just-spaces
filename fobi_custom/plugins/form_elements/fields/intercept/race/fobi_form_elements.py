from django import forms

from fobi.base import FormFieldPlugin, form_element_plugin_registry
from ..forms import RACE_CHOICES

from .forms import RaceForm


class RacePlugin(FormFieldPlugin):
    """RacePlugin."""

    uid = "race"
    name = "Which race or ethnicity best describes you?"
    form = RaceForm
    group = "Intercept"  # Group to which the plugin belongs to

    def get_form_field_instances(self, request=None, form_entry=None,
                                 form_element_entries=None, **kwargs):

        field_kwargs = {
            'required': self.data.required,
            'label': self.data.label,
            'widget': forms.widgets.RadioSelect(attrs={}),
            'choices': RACE_CHOICES,
        }

        return [(self.data.name, forms.ChoiceField, field_kwargs)]


form_element_plugin_registry.register(RacePlugin)
