from django.views.generic import TemplateView, ListView
from django.views.generic.edit import CreateView, FormView
from django.shortcuts import render, redirect

from pldp.models import Agency, Location, Study, Survey, SurveyRow, \
                        SurveyComponent
from fobi.models import FormEntry

from .models import JustSpacesUser
from .admin import JustSpacesUserCreationForm
from .forms import CreateStudyForm


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
    form_class = CreateStudyForm
    model = Study
    template_name = "study_create.html"
    success_url = '/'


class SurveyList(ListView):
    model = FormEntry
    template_name = "survey_list.html"
    context_object_name = 'surveys'


class SurveySubmittedList(TemplateView):
    template_name = "survey_submitted_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        surveys = Survey.objects.all()
        context['surveys_submitted'] = surveys.order_by('form_id', '-time_stop').distinct('form_id')

        for survey in context['surveys_submitted']:
            survey.form_title = FormEntry.objects.get(id=survey.form_id)

        return context


class SurveySubmittedDetail(TemplateView):
    template_name = "survey_submitted_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['form_entry'] = FormEntry.objects.get(id=context['form_entry_id'])
        context['surveys_submitted'] = Survey.objects.filter(form_id=context['form_entry_id'])

        for survey in context['surveys_submitted']:
            row = SurveyRow.objects.get(survey=survey)
            survey.row_total = row.total
            survey.components = SurveyComponent.objects.filter(row=row).order_by('position')

        first_survey = context['surveys_submitted'][0]
        context['questions'] = first_survey.components.values_list('label', flat=True)

        return context


class Signup(FormView):
    template_name = "registration/signup.html"
    form_class = JustSpacesUserCreationForm
    success_url = '/'

    def post(self, request):
        superuser = JustSpacesUser(is_superuser=True, is_staff=True)
        form = self.form_class(request.POST, instance=superuser)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            return redirect('login')

        return render(request, self.template_name, {'form': form})
