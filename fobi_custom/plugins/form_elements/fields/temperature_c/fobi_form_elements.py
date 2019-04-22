from django import forms

from fobi.base import FormFieldPlugin, form_element_plugin_registry, get_theme

from .forms import TemperatureCForm

theme = get_theme(request=None, as_instance=True)


class TemperatureCPlugin(FormFieldPlugin):
    """TemperatureCPlugin."""

    uid = "temperature_c"
    name = "Temperature, Celcius"
    form = TemperatureCForm
    group = "Survey Metadata"  # Group to which the plugin belongs to

    def get_form_field_instances(self, request=None, form_entry=None,
                                 form_element_entries=None, **kwargs):

        field_kwargs = {
            'required': self.data.required,
            'label': self.data.label,
            'widget': forms.widgets.NumberInput(attrs={
                                                    'class': theme.form_element_html_class,
                                                    'type': 'number'})
        }

        return [(self.data.name, forms.FloatField, field_kwargs)]


form_element_plugin_registry.register(TemperatureCPlugin)
