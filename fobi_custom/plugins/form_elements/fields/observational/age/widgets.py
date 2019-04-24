from django import forms
from fobi.base import FormElementPluginWidget


class BaseAgeObservationalPluginWidget(FormElementPluginWidget):
    """BaseAgeObservationalPluginWidget."""

    # Same as ``uid`` value of the ``AgeObservationalPlugin``.
    plugin_uid = "age_observational"

# based on: https://djangosnippets.org/snippets/1930/
options = 5

class AgeObservationalWidget(forms.MultiWidget):
    def __init__(self, *args, **kwargs):
        self.widgets = [forms.NumberInput()] * options

        super(AgeObservationalWidget, self).__init__(self.widgets, *args, **kwargs)

    def decompress(self, value):
        if value:
            return value.split(' ')
        return [None, None]
