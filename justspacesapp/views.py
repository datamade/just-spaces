from django.views.generic import TemplateView
from django.views.generic.edit import CreateView

from .forms import CreateAgencyForm, CreateLocationForm, \
                   CreateStudyForm, CreateSurveyForm


class CreateAgency(TemplateView):
    template_name = "create_agency.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CreateAgencyForm()
        return context


class CreateLocation(TemplateView):
    template_name = "create_location.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CreateLocationForm()
        return context


class CreateStudy(TemplateView):
    template_name = "create_study.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CreateStudyForm()
        return context


class CreateSurvey(TemplateView):
    template_name = "create_survey.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CreateSurveyForm()
        return context
