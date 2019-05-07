from datetime import datetime
import json

from django import forms

from leaflet.forms.widgets import LeafletWidget
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from pldp.models import Agency, Location, LocationArea, LocationLine, Study, \
                        StudyArea
from .models import SurveyFormEntry, SurveyChart


class JustSpacesForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(JustSpacesForm, self).__init__(*args, **kwargs)
        self.create_default_helper()

    def create_default_helper(self):
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))


class AgencyCreateForm(JustSpacesForm):
    class Meta:
        model = Agency
        fields = '__all__'


class LocationCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(LocationCreateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.form_method = 'post'
        self.helper.form_tag = False

        self.fields['agency'].initial = Agency.objects.first()
        self.fields['country'].initial = 'US'

    class Meta:
        model = Location
        fields = '__all__'

        leaflet_widget_attrs = {
            'map_height': '400px',
            'map_width': '100%',
        }

        widgets = {'geometry': LeafletWidget(attrs=leaflet_widget_attrs)}

        labels = {
            'name_primary': 'Primary name',
            'name_secondary': 'Secondary name'
        }


class LocationAreaCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(LocationAreaCreateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.form_method = 'post'
        self.helper.form_tag = False

        self.fields['location'].required = False
        self.fields['date_measured'].initial = datetime.now()

    class Meta:
        model = LocationArea
        fields = '__all__'

        widgets = {
            'location': forms.HiddenInput(),
            'date_measured': forms.DateInput(attrs={'type': 'date'}),
        }

        labels = {
            'date_measured': 'Area: Date Measured',
            'total_sqm': 'Area: Total sqm',
            'people_sqm': 'Area: People sqm',
            'typology': 'Area: Typology'
        }


class LocationLineCreateForm(JustSpacesForm):
    def __init__(self, *args, **kwargs):
        super(LocationLineCreateForm, self).__init__(*args, **kwargs)
        self.helper.form_tag = False
        self.fields['location'].required = False
        self.fields['date_measured'].initial = datetime.now()

    class Meta:
        model = LocationLine
        fields = '__all__'

        widgets = {
            'location': forms.HiddenInput(),
            'date_measured': forms.DateInput(attrs={'type': 'date'}),
        }

        labels = {
            'date_measured': 'Line: Date measured',
            'total_m': 'Line: Total width',
            'pedestrian_m': 'Line: Pedestrian width',
            'bicycle_m': 'Line: Bicycle width',
            'vehicular_m': 'Line: Vehicular width',
            'typology_pedestrian': 'Line: Pedestrian typology',
            'typology_bicycle': 'Line: Bicycle typology',
            'typology_vehicular': 'Line: Vehicular typology',
        }


class StudyAreaCreateForm(JustSpacesForm):
    class Meta:
        model = StudyArea
        fields = '__all__'

        leaflet_widget_attrs = {
            'map_height': '400px',
            'map_width': '100%',
        }

        widgets = {'area': LeafletWidget(attrs=leaflet_widget_attrs)}


class StudyCreateForm(JustSpacesForm):
    def __init__(self, *args, **kwargs):
        super(StudyCreateForm, self).__init__(*args, **kwargs)
        self.create_default_helper()
        self.fields['areas'].widget.attrs['class'] = 'basic-multiple'
        self.fields['agency'].initial = Agency.objects.first()

    class Meta:
        model = Study
        fields = '__all__'
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'})
        }


class SurveyCreateForm(JustSpacesForm):
    class Meta:
        model = SurveyFormEntry
        fields = ['user', 'name', 'study', 'location', 'type']


class FormElementEntryChoiceField(forms.ModelChoiceField):
    """
    A custom ModelChoiceField for Fobi FormElementEntry objects. Useful for
    allowing us to show a different label in the select widget.
    """
    def label_from_instance(self, obj):
        plugin_data = json.loads(obj.plugin_data)
        return plugin_data['label']


class SurveyChartForm(forms.ModelForm):
    class Meta:
        model = SurveyChart
        fields = ['short_description', 'order', 'source']
        widgets = {
            'order': forms.HiddenInput(),
        }
        field_classes = {
            'source': FormElementEntryChoiceField,
        }

    def __init__(self, *args, form_entry, **kwargs):
        self.form_entry = SurveyFormEntry.objects.get(id=form_entry)
        super().__init__(*args, **kwargs)
        self.fields['source'].queryset = self.form_entry.formelemententry_set.all()
