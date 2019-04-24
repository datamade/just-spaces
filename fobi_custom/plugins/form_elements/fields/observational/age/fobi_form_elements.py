from django import forms

from fobi.base import FormFieldPlugin, form_element_plugin_registry

from .forms import AgeObservationalForm
from .widgets import AgeObservationalWidget, options


class AgeObservationalPlugin(FormFieldPlugin):
    """AgeObservationalPlugin."""

    uid = "age_observational"
    name = "Age"
    form = AgeObservationalForm
    group = "Observational"  # Group to which the plugin belongs to

    def get_form_field_instances(self, request=None, form_entry=None,
                                 form_element_entries=None, **kwargs):

        field_kwargs = {
            'required': self.data.required,
            'label': self.data.label,
        }

        return [(self.data.name, AgeObservationalField, field_kwargs)]


class AgeObservationalField(forms.MultiValueField):
    widget = AgeObservationalWidget()

    def __init__(self, *args, **kwargs):
        fields = [forms.IntegerField()] * options
        
        super(AgeObservationalField, self).__init__(fields, *args, **kwargs)

    def compress(self, data_list):
        print("incoming data list: ")
        print(data_list)
        saved_data = sum(data_list)
        print("processed saved data: ")
        print(saved_data)
        return saved_data


form_element_plugin_registry.register(AgeObservationalPlugin)
