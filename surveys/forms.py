from django import forms
from leaflet.forms.widgets import LeafletWidget
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from pldp.models import Agency, Location, Study, StudyArea, Survey
from .models import SurveyFormEntry, SurveyChart

class CreateAgencyForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CreateAgencyForm, self).__init__(*args, **kwargs)
        create_default_helper(self)

    class Meta:
        model = Agency
        fields = '__all__'


class CreateLocationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CreateLocationForm, self).__init__(*args, **kwargs)
        create_default_helper(self)

    class Meta:
        model = Location
        fields = '__all__'


class StudyAreaCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(StudyAreaCreateForm, self).__init__(*args, **kwargs)
        create_default_helper(self)

    class Meta:
        model = StudyArea
        fields = '__all__'

        leaflet_widget_attrs = {
            'map_height': '400px',
            'map_width': '100%',
        }

        widgets = {'area': LeafletWidget(attrs=leaflet_widget_attrs)}


class StudyCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(StudyCreateForm, self).__init__(*args, **kwargs)
        create_default_helper(self)

    class Meta:
        model = Study
        fields = '__all__'
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'})
        }


class SurveyCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SurveyCreateForm, self).__init__(*args, **kwargs)
        create_default_helper(self)

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


def create_default_helper(self):
    self.helper = FormHelper()
    self.helper.form_class = 'form-horizontal'
    self.helper.label_class = 'col-lg-2'
    self.helper.field_class = 'col-lg-8'
    self.helper.form_method = 'post'
    self.helper.add_input(Submit('submit', 'Submit'))
