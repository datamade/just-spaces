import json

from django.views.generic import TemplateView, ListView, UpdateView, DetailView
from django.views.generic.edit import CreateView, FormView

from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
from django.forms import modelformset_factory
from django.contrib import messages

from pldp import models as pldp_models

from users.models import JustSpacesUser
from users.admin import JustSpacesUserCreationForm

from fobi.views import add_form_handler_entry

from . import forms as survey_forms
from .utils import get_or_none
from .models import SurveyFormEntry, SurveyChart, CensusArea, CensusObservation

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
    model = pldp_models.Location
    template_name = "location_list.html"
    context_object_name = 'locations'
    queryset = pldp_models.Location.objects.all().exclude(is_active=False)


class LocationDetail(DetailView):
    model = pldp_models.Location
    template_name = "location_detail.html"
    context_object_name = 'location'

    def get_context_data(self, **kwargs):
        context = super(LocationDetail, self).get_context_data(**kwargs)

        location = context['location']

        location_area = get_or_none(pldp_models.LocationArea, location=location)
        location_line = get_or_none(pldp_models.LocationLine, location=location)

        context['rows'] = [
            ('Region', location.region),
            ('City', location.city),
            ('Secondary name', location.name_secondary),
            ('Character', location.character),
            ('Geometry type', location.geometry_type),
        ]

        if location_area:
            context['rows'] += [
                ('Date measured', location_area.date_measured),
                ('Total sqm', location_area.total_sqm),
                ('People sqm', location_area.people_sqm),
                ('Typology', location_area.typology),
            ]

        if location_line:
            context['rows'] += [
                ('Date measured', location_line.date_measured),
                ('Total width', location_line.total_m),
                ('Pedestrian width', location_line.pedestrian_m),
                ('Bicycle width', location_line.bicycle_m),
                ('Vehicular width', location_line.vehicular_m),
                ('Pedestrian typology', location_line.typology_pedestrian),
                ('Bicycle typology', location_line.typology_bicycle),
                ('Vehicular typology', location_line.typology_vehicular),
            ]

        return context


class LocationDeactivate(TemplateView):
    template_name = "location_deactivate.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['location'] = pldp_models.Location.objects.get(id=context['pk'])

        return context

    def post(self, request, **kwargs):
        context = self.get_context_data(**kwargs)
        context['location'].is_active = False
        context['location'].save()

        return redirect('locations-list')


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


class StudyList(ListView):
    model = pldp_models.Study
    template_name = "study_list.html"
    context_object_name = 'studies'
    queryset = pldp_models.Study.objects.all().exclude(is_active=False)


class StudyDeactivate(TemplateView):
    template_name = "study_deactivate.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['study'] = pldp_models.Study.objects.get(id=context['pk'])

        return context

    def post(self, request, **kwargs):
        context = self.get_context_data(**kwargs)
        context['study'].is_active = False
        context['study'].save()

        return redirect('studies-list')


class StudyDetail(DetailView):
    model = pldp_models.Study
    template_name = "study_detail.html"
    context_object_name = 'study'

    def get_context_data(self, **kwargs):
        context = super(StudyDetail, self).get_context_data(**kwargs)
        study = context['study']

        context['rows'] = [
            ('Project', study.project),
            ('Project phase', study.project_phase),
            ('Start date', study.start_date),
            ('End date', study.end_date),
            ('Scale', study.scale),
            ('Manager email', study.manager_email),
            ('Protocol version', study.protocol_version),
            ('Notes', study.notes),
        ]

        return context


class SurveyCreate(CreateView):
    form_class = survey_forms.SurveyCreateForm
    model = SurveyFormEntry
    template_name = "survey_create.html"

    def get_initial(self):
        self.initial['user'] = self.request.user
        return self.initial.copy()

    def get_context_data(self, **kwargs):
        context = super(SurveyCreate, self).get_context_data(**kwargs)

        url_studies_list = reverse_lazy('studies-list')
        url_studies_create = reverse_lazy('studies-create')
        study_help_text = 'Don\'t see the study you need? View the \
                           <a href="{}">list of existing studies</a> or \
                           <a href="{}">create a new \
                           one</a>.'.format(url_studies_list, url_studies_create)

        context['form'].fields['study'].help_text += study_help_text

        url_locations_list = reverse_lazy('locations-list')
        url_locations_create = reverse_lazy('locations-create')
        location_help_text = 'Don\'t see the location you need? View the \
                           <a href="{}">list of existing locations</a> or \
                           <a href="{}">create a new \
                           one</a>.'.format(url_locations_list, url_locations_create)

        context['form'].fields['location'].help_text += location_help_text

        return context

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

        # Fobi types, bins, and ACS variables for use in charting
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
        context['acs_compatible_types'] = json.dumps(
            list(fobi_types.TYPES_TO_ACS_VARIABLES.keys())
        )

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


def census_area_to_observation(request):
    """
    API endpoint returning ACS data for a given CensusArea and ACS variable.

    :param request: A Django HTTPRequest object. Requires a census_area param and
                    a primary_source param, or else will return 400.
    :returns: A JsonResponse representing the data in question. If no CensusArea
              object matches census_area, returns HTTP status 404 with a message
              in the 'error' key. Otherwise, returns the data in the 'data' key.
    """
    # Check the query parameters
    census_area_id = request.GET.get('census_area')
    primary_source_id = request.GET.get('primary_source')
    if not census_area_id or not primary_source_id:
        return JsonResponse(
            {'error': 'census_area and primary_source are required query parameters'},
            status=400
        )

    response = {}
    try:
        census_area = CensusArea.objects.get(id=census_area_id)
    except CensusArea.DoesNotExist:
        response['error'] = 'No CensusArea object found for ID {}'.format(
            str(census_area_id)
        )
        status = 400
    else:
        try:
            response['data'] = census_area.get_observations_from_component(primary_source_id)
        except CensusObservation.DoesNotExist as e:
            response['error'] = str(e)
            status = 400
        else:
            status = 200

    return JsonResponse(response, status=status)
