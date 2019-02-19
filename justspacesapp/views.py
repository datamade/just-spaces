from django.views.generic import TemplateView
from django.views.generic.edit import CreateView

from .forms import CreateStudyForm, CreateSurveyForm

from pldp.models import Agency, Location, Study


class CreateAgency(CreateView):
    model = Agency
    template_name = "create_agency.html"
    fields = '__all__'
    success_url = '/'

class CreateLocation(CreateView):
    model = Location
    template_name = "create_location.html"
    fields = '__all__'
    success_url = '/'

class CreateStudy(CreateView):
    model = Study
    template_name = "create_study.html"
    fields = '__all__'
    success_url = '/'

class CreateSurvey(TemplateView):
    # to create a sample area:
    # INSERT INTO pldp_studyarea (name, area) VALUES ('Example area', ST_SetSRID(ST_MakePoint(1,2),4326));

    template_name = "create_survey.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CreateSurveyForm()
        return context
