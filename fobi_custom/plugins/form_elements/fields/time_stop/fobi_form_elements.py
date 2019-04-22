from django import forms

from fobi.base import FormFieldPlugin, form_element_plugin_registry, get_theme

from .forms import TimeStopForm

theme = get_theme(request=None, as_instance=True)


class TimeStopPlugin(FormFieldPlugin):
    """TimeStopPlugin."""

    uid = "time_stop"
    name = "Stop Time"
    form = TimeStopForm
    group = "Survey Metadata"  # Group to which the plugin belongs to

    def get_form_field_instances(self, request=None, form_entry=None,
                                 form_element_entries=None, **kwargs):

        field_kwargs = {
            'required': self.data.required,
            'label': self.data.label,
            'widget': forms.widgets.TextInput(attrs={'class': theme.form_element_html_class, 'type': 'time'}),
        }

        return [(self.data.name, forms.TimeField, field_kwargs)]


form_element_plugin_registry.register(TimeStopPlugin)
