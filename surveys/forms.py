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
        self.fields['name_primary'].label = "Primary name"
        self.fields['name_secondary'].label = "Secondary name"

    class Meta:
        model = Location
        fields = '__all__'

        leaflet_widget_attrs = {
            'map_height': '400px',
            'map_width': '100%',
        }

        widgets = {'geometry': LeafletWidget(attrs=leaflet_widget_attrs)}


class LocationAreaCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(LocationAreaCreateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.form_method = 'post'
        self.helper.form_tag = False

        self.fields['date_measured'].label = "Area: Date Measured"
        self.fields['total_sqm'].label = "Area: Total sqm"
        self.fields['people_sqm'].label = "Area: People sqm"
        self.fields['typology'].label = "Area: Typology"

        self.fields['location'].required = False

    class Meta:
        model = LocationArea
        fields = '__all__'  # ['date_measured', 'total_sqm', 'people_sqm', 'typology']

        widgets = {
            'location': forms.HiddenInput(),
            'date_measured': forms.DateInput(attrs={'type': 'date'}),
        }


class LocationLineCreateForm(JustSpacesForm):
    def __init__(self, *args, **kwargs):
        super(LocationLineCreateForm, self).__init__(*args, **kwargs)
        self.helper.form_tag = False

        self.fields['date_measured'].label = "Line: Date Measured"
        self.fields['total_m'].label = "Line: Total width"
        self.fields['pedestrian_m'].label = "Line: Pedestrian width"
        self.fields['bicycle_m'].label = "Line: Bicycle width"
        self.fields['vehicular_m'].label = "Line: Vehicular width"
        self.fields['typology_pedestrian'].label = "Line: Pedestrian typology"
        self.fields['typology_bicycle'].label = "Line: Bicycle typology"
        self.fields['typology_vehicular'].label = "Line: Vehicular typology"

        self.fields['location'].required = False

    class Meta:
        model = LocationLine
        fields = '__all__'

        widgets = {
            'location': forms.HiddenInput(),
            'date_measured': forms.DateInput(attrs={'type': 'date'}),
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


class SurveyChartForm(forms.ModelForm):
    class Meta:
        model = SurveyChart
        fields = ['short_description', 'order']
        widgets = {
            'order': forms.HiddenInput()
        }

    def __init__(self, *args, form_entry, **kwargs):
        self.form_entry = SurveyFormEntry.objects.get(id=form_entry)
        super().__init__(*args, **kwargs)
