from django.views.generic import TemplateView, ListView
from django.views.generic.edit import CreateView, FormView
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.forms import modelformset_factory
from django.contrib import messages

from pldp.models import Agency, Location, Study, Survey

from users.models import JustSpacesUser
from users.admin import JustSpacesUserCreationForm

from fobi.views import add_form_handler_entry

from .models import SurveyFormEntry, SurveyChart
from .forms import StudyCreateForm, SurveyCreateForm, SurveyChartForm


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

    def form_valid(self, form):
        self.object = form.save()

        # this adds our custom collect_data plugin as default data handler
        add_form_handler_entry(self.request,
                               self.object.formentry_ptr_id,
                               'collect_data'
                               )

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        form_entry_id = self.object.formentry_ptr_id
        success_url = reverse_lazy('fobi.edit_form_entry', kwargs={'form_entry_id': form_entry_id})

        return str(success_url)


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

        return redirect('surveys-list-run')


class SurveyListEdit(ListView):
    model = SurveyFormEntry
    template_name = "survey_list.html"
    context_object_name = 'surveys'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['surveys'] = context['surveys'].filter(published=False).order_by('-updated')
        context['published'] = False

        return context


class SurveyListRun(ListView):
    model = SurveyFormEntry
    template_name = "survey_list.html"
    context_object_name = 'surveys'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['surveys'] = context['surveys'].filter(published=True).order_by('-updated')
        context['published'] = True

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
    ChartFormset = ChartFormset = modelformset_factory(SurveyChart,
                                                       form=SurveyChartForm,
                                                       exclude=('form_entry',),
                                                       can_order=True,
                                                       can_delete=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['form_entry'] = SurveyFormEntry.objects.get(id=context['form_entry_id'])
        context['surveys_submitted'] = Survey.objects.filter(form_id=context['form_entry_id'])

        first_survey = context['surveys_submitted'][0]
        context['questions'] = first_survey.components.values_list('label', flat=True)

        context['chart_formset'] = self.ChartFormset(
            queryset=SurveyChart.objects.filter(form_entry=context['form_entry']),
            form_kwargs={'form_entry': context['form_entry_id']},
        )

        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        formset = self.ChartFormset(
            request.POST,
            form_kwargs={'form_entry': context['form_entry_id']}
        )
        if formset.is_valid():
            for form in formset:
                # Wait to commit the SurveyChart until we can assign it a
                # form_entry ID.
                survey_chart = form.save(commit=False)
                survey_chart.form_entry = form.form_entry
                survey_chart.save()

                messages.add_message(request, messages.INFO, 'Charts saved!')

        context['chart_formset'] = formset
        return render(request, self.template_name, context)


class Signup(FormView):
    template_name = "registration/signup.html"
    form_class = JustSpacesUserCreationForm
    success_url = '/'

    def post(self, request):
        superuser = JustSpacesUser(is_superuser=True, is_staff=True)
        form = self.form_class(request.POST, instance=superuser)
        if form.is_valid():
            form.save()
            return redirect('login')

        return render(request, self.template_name, {'form': form})
