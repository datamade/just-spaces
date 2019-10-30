from datetime import datetime

from django import forms

from leaflet.forms.widgets import LeafletWidget
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

import pldp.models as pldp_models

from fobi_custom.plugins.form_elements.fields import types as fobi_types
from . import models as survey_models
from surveys import widgets


class JustSpacesForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(JustSpacesForm, self).__init__(*args, **kwargs)
        self.create_default_helper()

    def create_default_helper(self):
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-9'
        self.helper.form_method = 'post'
        self.add_inputs(self.helper)

    def add_inputs(self, helper):
        helper.add_input(Submit('submit', 'Submit', css_class='float-right'))


class AgencyCreateForm(JustSpacesForm):
    class Meta:
        model = pldp_models.Agency
        fields = '__all__'

        widgets = {
            'is_active': forms.HiddenInput()
        }


class LocationCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(LocationCreateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-9'
        self.helper.form_method = 'post'
        self.helper.form_tag = False

        self.fields['country'].initial = 'US'

    class Meta:
        model = pldp_models.Location
        fields = '__all__'

        leaflet_widget_attrs = {
            'map_height': '400px',
            'map_width': '100%',
        }

        widgets = {
            'geometry': LeafletWidget(attrs=leaflet_widget_attrs),
            'is_active': forms.HiddenInput()
        }

        labels = {
            'name_primary': 'Primary name',
            'name_secondary': 'Secondary name'
        }


class LocationAreaCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(LocationAreaCreateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-9'
        self.helper.form_method = 'post'
        self.helper.form_tag = False

        self.fields['location'].required = False
        self.fields['date_measured'].initial = datetime.now()

    class Meta:
        model = pldp_models.LocationArea
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
        model = pldp_models.LocationLine
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
        model = pldp_models.StudyArea
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

        self.fields['agency'].queryset = pldp_models.Agency.objects.filter(is_active='t')

        self.fields['title'].required = True

    class Meta:
        model = pldp_models.Study
        fields = '__all__'
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'is_active': forms.HiddenInput()
        }


class SurveyCreateForm(JustSpacesForm):
    def __init__(self, *args, **kwargs):
        agency = kwargs.pop('agency')
        super(SurveyCreateForm, self).__init__(*args, **kwargs)
        self.fields['study'].required = True
        self.fields['study'].queryset = pldp_models.Study.objects.filter(is_active='t')
        if agency:
            self.fields['study'].queryset = self.fields['study'].queryset.filter(agency=agency)

        self.fields['location'].required = True
        self.fields['location'].queryset = pldp_models.Location.objects.filter(is_active='t')

        self.fields['name'].help_text = "Survey names should be unique and memorable."
        self.fields['type'].help_text = "This selection will determine which questions \
                                        are available to add to your survey."
        self.fields['survey_template'].help_text = "Choose a template if you'd like to \
                                                   prepopulate your survey with a set of \
                                                   recommended questions. You'll still be  \
                                                   able to edit them on the next screen."

    class Meta:
        model = survey_models.SurveyFormEntry
        fields = ['user', 'name', 'study', 'location', 'type', 'survey_template', 'active']
        widgets = {
            'user': forms.HiddenInput(),
            'active': forms.HiddenInput(),
        }

    def clean_survey_template(self):
        template = self.cleaned_data['survey_template']
        survey_type = self.cleaned_data['type']

        if template and (template.surveyformentry.type != survey_type):
            raise forms.ValidationError(
                "Make sure you choose an {0} template to create a new {0} survey!".format(survey_type)
            )

        return template


class SurveyEditForm(JustSpacesForm):
    def __init__(self, *args, **kwargs):
        super(SurveyEditForm, self).__init__(*args, **kwargs)
        self.fields['study'].required = True
        self.fields['location'].required = True

    class Meta:
        model = survey_models.SurveyFormEntry
        fields = ['user', 'name', 'study', 'location', 'type', 'active']
        widgets = {
            'user': forms.HiddenInput(),
            'type': forms.HiddenInput(),
            'active': forms.HiddenInput(),
        }


class CensusAreaRegionSelectForm(JustSpacesForm):
    class Meta:
        model = survey_models.CensusArea
        fields = ['name', 'region']

    def add_inputs(self, helper):
        # Override base method to remove Submit button from this form.
        return None


class CensusAreaCreateForm(JustSpacesForm):
    use_required_attribute = False
    restrict_by_agency = forms.BooleanField(
        label='Restrict to my agency',
        initial=False,
        help_text=(
            'This will make this CensusArea viewable only by you and members '
            'of your agency. If this box is unchecked, all users will be able '
            'to find and use your CensusArea for their own analyses.'
        ),
        required=False
    )

    class Meta:
        model = survey_models.CensusArea
        fields = ['name', 'region', 'fips_codes', 'restrict_by_agency']
        widgets = {
            'fips_codes': widgets.MultiSelectGeometryWidget(),
        }

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.fields['fips_codes'].widget.choices = [
            (choice.fips_code, choice) for choice
            in survey_models.CensusBlockGroup.objects.all()
        ]
        if self.instance.agency:
            self.fields['restrict_by_agency'].initial = True

    def save(self, commit=True):
        if self.cleaned_data['restrict_by_agency'] is True:
            self.instance.agency = self.user.agency
        else:
            self.instance.agency = None
        return super().save(commit=commit)


class CensusAreaEditForm(CensusAreaCreateForm):
    class Meta:
        model = survey_models.CensusArea
        fields = ['name', 'fips_codes', 'restrict_by_agency']
        widgets = {
            'fips_codes': widgets.MultiSelectGeometryWidget(),
        }


class SurveyChartForm(forms.ModelForm):
    class Meta:
        model = survey_models.SurveyChart
        fields = ['short_description', 'order', 'primary_source', 'census_areas']
        widgets = {
            'order': forms.HiddenInput(),
            'primary_source': forms.Select(),
        }

    def __init__(self, *args, form_entry, **kwargs):
        self.form_entry = survey_models.SurveyFormEntry.objects.get(id=form_entry)
        super().__init__(*args, **kwargs)
        survey = pldp_models.Survey.objects.filter(form_id=form_entry)[0]
        choices = [(component.name, component.label) for component in survey.components
                   if component.type in fobi_types.ALL_VALID_TYPES]
        choices = [('', '-----')] + choices  # Offer a null choice
        self.fields['primary_source'].widget.choices = choices
