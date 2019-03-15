from django import forms
from pldp.models import Agency, Location, Study, Survey


class CreateAgencyForm(forms.ModelForm):
    class Meta:
        model = Agency
        fields = '__all__'


class CreateLocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = '__all__'


class CreateStudyForm(forms.ModelForm):
    class Meta:
        model = Study
        fields = '__all__'


class CreateSurveyForm(forms.ModelForm):
    class Meta:
        model = Survey
        fields = '__all__'
