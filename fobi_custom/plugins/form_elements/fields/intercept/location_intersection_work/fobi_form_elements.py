from django import forms

from fobi.base import FormFieldPlugin, form_element_plugin_registry

from .forms import LocationIntersectionWorkForm


class LocationIntersectionWorkPlugin(FormFieldPlugin):
    """LocationIntersectionWorkPlugin."""

    uid = "location_intersection_work"
    name = "What is the closest intersection to your workplace?"
    form = LocationIntersectionWorkForm
    group = "Intercept"  # Group to which the plugin belongs to

    def get_form_field_instances(self, request=None, form_entry=None,
                                 form_element_entries=None, **kwargs):

        field_kwargs = {
            'required': self.data.required,
            'label': self.data.label,
            'widget': forms.widgets.TextInput(attrs={}),
        }

        return [(self.data.name, forms.CharField, field_kwargs)]


form_element_plugin_registry.register(LocationIntersectionWorkPlugin)
