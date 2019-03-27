from django import forms
from django.utils.translation import ugettext_lazy as _
from fobi.base import BasePluginForm

class CollectDataForm(forms.Form, BasePluginForm):
    """Mail form."""

    plugin_data_fields = [
        ("from_name", ""),
        ("from_email", ""),
        ("to_name", ""),
        ("to_email", ""),
        ("subject", ""),
        ("body", ""),
    ]

    from_name = forms.CharField(label=_("From name"), required=True)
    from_email = forms.EmailField(label=_("From email"), required=True)
    to_name = forms.CharField(label=_("To name"), required=True)
    to_email = forms.EmailField(label=_("To email"), required=True)
    subject = forms.CharField(label=_("Subject"), required=True)
    body = forms.CharField(
        label=_("Body"),
        required=False,
        widget=forms.widgets.Textarea
    )
