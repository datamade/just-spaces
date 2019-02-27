from django import forms

from fobi.base import BasePluginForm
from pldp.forms import AGE_TYPE_CHOICES

import uuid


class PLDPAgeSingleForm(forms.Form, BasePluginForm):
    """PLDPAgeSingleForm."""

    plugin_data_fields = [
        ("label", ""),
        ("name", uuid.uuid4()),
        ("required", False),
        ("detail_level", "basic")
    ]

    label = forms.CharField(label="Label", required=True)
    name = forms.CharField(required=True, widget=forms.widgets.HiddenInput())
    required = forms.BooleanField(label="Required", required=False)
    detail_level = forms.ChoiceField(choices=AGE_TYPE_CHOICES,
                                     help_text="The Public Life Data Protocol "
                                     "suggests collecting age data at one "
                                     "of three levels of detail:<br /><br />"
                                     "<b>Basic</b><br />"
                                     "0-14<br />"
                                     "15-24<br />"
                                     "25-64<br />"
                                     "65+<br /><br />"
                                     "<b>Detailed</b><br />"
                                     "0-4<br />"
                                     "5-14<br />"
                                     "15-24<br />"
                                     "25-44<br />"
                                     "45-64<br />"
                                     "65-74<br />"
                                     "75+<br /><br />"
                                     "<b>Complex</b><br />"
                                     "0-4<br />"
                                     "5-9<br />"
                                     "10-14<br />"
                                     "15-17<br />"
                                     "18-24<br />"
                                     "25-34<br />"
                                     "35-44<br />"
                                     "45-54<br />"
                                     "55-64<br />"
                                     "65-74<br />"
                                     "75+<br /><br />")
