import sys
from fobi.base import FormFieldPlugin, form_element_plugin_registry
from pldp.forms import GROUPS_BASIC_CHOICES

from ..widgets import ObservationalWidget
from ..fields import ObservationalField

from .forms import GroupsObservationalForm


class GroupsObservationalPlugin(FormFieldPlugin):
    """GroupsObservationalPlugin."""

    uid = "groups_observational"
    name = "Group Size"
    form = GroupsObservationalForm
    group = "Observational"  # Group to which the plugin belongs to

    def get_form_field_instances(self, request=None, form_entry=None,
                                 form_element_entries=None, **kwargs):

        choices = GROUPS_BASIC_CHOICES

        field_kwargs = {
            'required': self.data.required,
            'label': self.data.label,
            'choices': choices,
            'widget': ObservationalWidget(choices=choices)
        }

        return [(self.data.name, ObservationalField, field_kwargs)]


form_element_plugin_registry.register(GroupsObservationalPlugin)
