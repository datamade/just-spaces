from fobi.base import FormFieldPlugin, form_element_plugin_registry
from fobi_custom.plugins.form_elements.fields.intercept.forms import RACE_CHOICES

from ..widgets import ObservationalWidget
from ..fields import ObservationalField

from .forms import RaceObservationalForm


class RaceObservationalPlugin(FormFieldPlugin):
    """RaceObservationalPlugin."""

    uid = "race_observational"
    name = "Perceived Race"
    form = RaceObservationalForm
    group = "Observational"  # Group to which the plugin belongs to

    def get_form_field_instances(self, request=None, form_entry=None,
                                 form_element_entries=None, **kwargs):

        field_kwargs = {
            'required': self.data.required,
            'label': self.data.label,
            'choices': RACE_CHOICES,
            'widget': ObservationalWidget(choices=RACE_CHOICES)
        }

        return [(self.data.name, ObservationalField, field_kwargs)]


form_element_plugin_registry.register(RaceObservationalPlugin)
