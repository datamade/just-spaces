from django.views.generic import TemplateView, ListView, View
from django.views.generic.edit import CreateView, FormView
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect

from pldp.models import Agency, Location, Study, Survey

from users.models import JustSpacesUser
from users.admin import JustSpacesUserCreationForm

from fobi.views import add_form_handler_entry

from .models import SurveyFormEntry
from .forms import StudyCreateForm, SurveyCreateForm


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
    form_class = StudyCreateForm
    model = Study
    template_name = "study_create.html"
    success_url = '/'


class SurveyCreate(CreateView):
    form_class = SurveyCreateForm
    model = SurveyFormEntry
    template_name = "survey_create.html"
    success_url = '/'

    def form_valid(self, form):
        self.object = form.save()

        # this adds our custom collect_data plugin as default data handler
        add_form_handler_entry(self.request,
                               self.object.formentry_ptr_id,
                               'collect_data'
                               )

        return HttpResponseRedirect(self.get_success_url())


class SurveyPublish(TemplateView):
    template_name = "survey_publish.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['survey'] = SurveyFormEntry.objects.get(id=context['form_entry_id'])

        return context

    def post(self, request, **kwargs):
        context = self.get_context_data(**kwargs)
        context['survey'].published = True
        context['survey'].save()

        return redirect('surveys-list')


class SurveyList(ListView):
    model = SurveyFormEntry
    template_name = "survey_list.html"
    context_object_name = 'surveys'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['published'] = self.request.GET.get('published', 'f')
        context['surveys'] = context['surveys'].filter(published=context['published'])

        return context


class SurveySubmittedList(TemplateView):
    template_name = "survey_submitted_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        surveys = Survey.objects.all()
        context['surveys_submitted'] = surveys.order_by('form_id', '-time_stop').distinct('form_id')

        for survey in context['surveys_submitted']:
            try:
                survey_form_entry = SurveyFormEntry.objects.get(formentry_ptr=survey.form_id)
                survey.form_title = survey_form_entry.name
            except SurveyFormEntry.DoesNotExist:
                survey.form_title = "[Deleted Survey]"

        return context


class SurveySubmittedDetail(TemplateView):
    template_name = "survey_submitted_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['form_entry'] = SurveyFormEntry.objects.get(id=context['form_entry_id'])
        context['surveys_submitted'] = Survey.objects.filter(form_id=context['form_entry_id'])

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
