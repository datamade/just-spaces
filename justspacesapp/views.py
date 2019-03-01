from django.views.generic import ListView
from django.views.generic.edit import CreateView

from pldp.models import Agency, Location, Study
from fobi.models import FormEntry


class AgencyCreate(CreateView):
    model = Agency
    template_name = "agency_create.html"
    fields = '__all__'
    success_url = '/'


class LocationCreate(CreateView):
    model = Location
    template_name = "location_create.html"
    fields = '__all__'
    success_url = '/'


class StudyCreate(CreateView):
    model = Study
    template_name = "study_create.html"
    fields = '__all__'
    success_url = '/'


class SurveyList(ListView):
    model = FormEntry
    template_name = "survey_list.html"
    context_object_name = 'surveys'
