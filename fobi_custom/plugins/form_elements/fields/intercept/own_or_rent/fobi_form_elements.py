from django import forms

from fobi.base import FormFieldPlugin, form_element_plugin_registry
from ..forms import OWN_OR_RENT_CHOICES

from .forms import OwnOrRentForm


class OwnOrRentPlugin(FormFieldPlugin):
    """OwnOrRentPlugin."""

    uid = "own_or_rent"
    name = "Are you a homeowner or a renter?"
    form = OwnOrRentForm
    group = "Intercept"  # Group to which the plugin belongs to

    def get_form_field_instances(self, request=None, form_entry=None,
                                 form_element_entries=None, **kwargs):

        field_kwargs = {
            'required': self.data.required,
            'label': self.data.label,
            'widget': forms.widgets.Select(attrs={}),
            'choices': OWN_OR_RENT_CHOICES,
        }

        return [(self.data.name, forms.ChoiceField, field_kwargs)]


form_element_plugin_registry.register(OwnOrRentPlugin)
