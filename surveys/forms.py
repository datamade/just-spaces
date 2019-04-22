from django import forms
from pldp.models import Agency, Location, Study, Survey
from .models import SurveyFormEntry, SurveyChart


class CreateAgencyForm(forms.ModelForm):
    class Meta:
        model = Agency
        fields = '__all__'


class CreateLocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = '__all__'


class StudyCreateForm(forms.ModelForm):
    class Meta:
        model = Study
        fields = '__all__'
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'})
        }


class SurveyCreateForm(forms.ModelForm):
    class Meta:
        model = SurveyFormEntry
        fields = ['user', 'name', 'study', 'location', 'type']


class SurveyChartForm(forms.ModelForm):
    class Meta:
        model = SurveyChart
        fields = ['short_description']
