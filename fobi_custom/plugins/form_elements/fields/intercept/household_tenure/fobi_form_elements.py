from django import forms

from fobi.base import FormFieldPlugin, form_element_plugin_registry

from .forms import HouseholdTenureForm


class HouseholdTenurePlugin(FormFieldPlugin):
    """HouseholdTenurePlugin."""

    uid = "household_tenure"
    name = "What year did you move into your current address?"
    form = HouseholdTenureForm
    group = "Intercept"  # Group to which the plugin belongs to

    def get_form_field_instances(self, request=None, form_entry=None,
                                 form_element_entries=None, **kwargs):

        field_kwargs = {
            'required': self.data.required,
            'label': self.data.label,
            'widget': forms.widgets.NumberInput(attrs={}),
        }

        return [(self.data.name, forms.IntegerField, field_kwargs)]


form_element_plugin_registry.register(HouseholdTenurePlugin)
