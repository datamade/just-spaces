import json

from django.views.generic import TemplateView, ListView, UpdateView, DetailView
from django.views.generic.edit import CreateView, FormView, DeleteView
from django.views.generic.detail import SingleObjectTemplateResponseMixin

from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.forms import modelformset_factory
from django.contrib import messages

from pldp import models as pldp_models

from users.models import JustSpacesUser
from users.admin import JustSpacesUserCreationForm

from fobi.views import add_form_handler_entry

from .models import SurveyFormEntry, SurveyChart
from surveys import forms as survey_forms

from fobi_custom.plugins.form_elements.fields import types as fobi_types


class AgencyCreate(CreateView):
    form_class = survey_forms.AgencyCreateForm
    model = pldp_models.Agency
    template_name = "agency_create.html"
    success_url = '/'


class LocationCreate(CreateView):
    form_class = survey_forms.LocationCreateForm
    form_class_location_area = survey_forms.LocationAreaCreateForm
    form_class_location_line = survey_forms.LocationLineCreateForm

    template_name = "location_create.html"
    success_url = reverse_lazy('locations-list')

    def get_context_data(self, **kwargs):
        context = super(LocationCreate, self).get_context_data(**kwargs)

        context['form_location'] = self.form_class(prefix="location")
        context['form_location_area'] = self.form_class_location_area(prefix="location-area")
        context['form_location_line'] = self.form_class_location_line(prefix="location-line")

        return context

    def post(self, request, **kwargs):
        form_location = self.form_class(request.POST, prefix="location")
        form_location_area = self.form_class_location_area(request.POST, prefix="location-area")
        form_location_line = self.form_class_location_line(request.POST, prefix="location-line")

        if request.POST['location-geometry_type'] == 'area':
            forms_valid = [form_location.is_valid(), form_location_area.is_valid()]

            if all(forms_valid):
                location = form_location.save()
                form_location_area.cleaned_data.pop('location')

                location_area = pldp_models.LocationArea(
                                    location=location,
                                    **form_location_area.cleaned_data
                                )
                location_area.save()
                return redirect(self.success_url)

        elif request.POST['location-geometry_type'] == 'line':
            forms_valid = [form_location.is_valid(), form_location_line.is_valid()]

            if all(forms_valid):
                location = form_location.save()
                form_location_line.cleaned_data.pop('location')

                location_line = pldp_models.LocationLine(
                                    location=location,
                                    **form_location_line.cleaned_data
                                )
                location_line.save()
                return redirect(self.success_url)

        else:
            if form_location.is_valid():
                form_location.save()
                return redirect(self.success_url)

        return render(request,
                      'location_create.html',
                      {'form_location': form_location,
                       'form_location_area': form_location_area,
                       'form_location_line': form_location_line}
                      )


class LocationList(ListView):
    model = Location
    template_name = "location_list.html"
    context_object_name = 'locations'


class LocationDetail(DetailView):
    model = Location
    template_name = "location_detail.html"
    context_object_name = 'location'


class LocationDelete(DeleteView):
    model = Location
    template_name = "location_delete.html"
    success_url = reverse_lazy('locations-list')


class StudyAreaCreate(CreateView):
    form_class = survey_forms.StudyAreaCreateForm
    model = pldp_models.StudyArea
    template_name = "study_area_create.html"
    success_url = reverse_lazy('studies-create')


class StudyCreate(CreateView):
    form_class = survey_forms.StudyCreateForm
    model = pldp_models.Study
    template_name = "study_create.html"
    success_url = reverse_lazy('surveys-list-edit')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        url = reverse_lazy('study-areas-create')
        extra_help_text = ' Don\'t see the area you need? <a href="{}" target="_blank">Create a new one here</a>'.format(url)
        context['form'].fields['areas'].help_text += extra_help_text

        return context


class SurveyCreate(CreateView):
    form_class = survey_forms.SurveyCreateForm
    model = SurveyFormEntry
    template_name = "survey_create.html"

    def get_initial(self):
        self.initial['user'] = self.request.user
        return self.initial.copy()

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

        return success_url


class SurveyPropertiesEdit(UpdateView):
    model = SurveyFormEntry
    template_name = "survey_properties_edit.html"
    form_class = survey_forms.SurveyCreateForm
    context_object_name = 'form_object'

    def get_success_url(self):
        form_entry_id = self.object.pk
        success_url = reverse_lazy('fobi.edit_form_entry', kwargs={'form_entry_id': form_entry_id})

        return success_url


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

        surveys = pldp_models.Survey.objects.all()
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
    ChartFormset = modelformset_factory(SurveyChart,
                                        form=survey_forms.SurveyChartForm,
                                        exclude=('form_entry',),
                                        extra=0,
                                        can_delete=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['form_entry'] = SurveyFormEntry.objects.get(id=context['form_entry_id'])
        context['surveys_submitted'] = pldp_models.Survey.objects.filter(form_id=context['form_entry_id'])

        # Generate a JSON representation of survey data for use in charting
        surveys_submitted_json = []
        for survey in context['surveys_submitted']:
            surveys_submitted_json.append({
                'time_start': survey.time_start,
                'time_stop': survey.time_stop,
                'data': {component.name: {
                            'type': component.type,
                            'value': component.saved_data
                        } for component in survey.components}
            })
        context['surveys_submitted_json'] = json.dumps(surveys_submitted_json,
                                                       default=str)

        # Fobi types and bins for use in charting
        types = {
            'count': fobi_types.COUNT_TYPES,
            'observational': fobi_types.OBSERVATIONAL_TYPES,
            'observationalCount': fobi_types.OBSERVATIONAL_COUNT_TYPES,
            'intercept': fobi_types.INTERCEPT_TYPES,
            'freeResponseIntercept': fobi_types.FREE_RESPONSE_INTERCEPT_TYPES,
        }
        bins = {
            'freeResponseIntercept': fobi_types.FREE_RESPONSE_INTERCEPT_BINS,
        }
        context['types'] = json.dumps(types)
        context['bins'] = json.dumps(bins)

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
            form_kwargs={'form_entry': kwargs['form_entry_id']}
        )
        if formset.is_valid():
            for form in formset:
                if form.cleaned_data.get('DELETE'):
                    # If the chart has already been saved, it will have a unique
                    # ID, and we need to delete it from the database.
                    if form.cleaned_data.get('id') is not None:
                        survey_chart = form.save(commit=False)
                        survey_chart.delete()
                    else:
                        # This is an empty form field
                        continue
                else:
                    # Wait to commit the SurveyChart until we can assign it a
                    # form_entry ID.
                    survey_chart = form.save(commit=False)
                    survey_chart.form_entry = form.form_entry
                    survey_chart.save()
            messages.success(request, 'Charts saved!')
        else:
            messages.error(request, 'Chart validation failed! See charts below for more detail.')
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
