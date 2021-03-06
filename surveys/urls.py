"""justspaces URL Configuration

Many of the following views are taken from django-fobi, and follow their
naming url patterns. As this app grows in complexity, we may want to
refigure it to a more strictful RESTful approach.

"""
from django.conf.urls import url, include
from django.urls import path
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.decorators import login_required

from surveys import views as survey_views
from .utils import staff_required_custom_login

import fobi.views

urlpatterns = [
    url(r'^$',
        survey_views.About.as_view(),
        name='home'),

    url(r'^accounts/',
        include('django.contrib.auth.urls')),

    url(r'agencies/$',
        staff_required_custom_login(survey_views.AgencyList.as_view()),
        name='agencies-list'),

    url(r'agencies/create/$',
        staff_required_custom_login(survey_views.AgencyCreate.as_view()),
        name='agencies-create'),

    url(r'agencies/deactivate/(?P<pk>[\w_\-]+)/$',
        staff_required_custom_login(survey_views.AgencyDeactivate.as_view()),
        name='agencies-deactivate'),

    url(r'agencies/(?P<pk>[\w_\-]+)/$',
        staff_required_custom_login(survey_views.AgencyDetail.as_view()),
        name='agencies-detail'),

    url(r'locations/create/$',
        staff_required_custom_login(survey_views.LocationCreate.as_view()),
        name='locations-create'),

    url(r'locations/$',
        staff_required_custom_login(survey_views.LocationList.as_view()),
        name='locations-list'),

    url(r'locations/deactivate/(?P<pk>[\w_\-]+)/$',
        staff_required_custom_login(survey_views.LocationDeactivate.as_view()),
        name='locations-deactivate'),

    url(r'locations/(?P<pk>[\w_\-]+)/$',
        staff_required_custom_login(survey_views.LocationDetail.as_view()),
        name='locations-detail'),

    url(r'study-areas/create/$',
        staff_required_custom_login(survey_views.StudyAreaCreate.as_view()),
        name='study-areas-create'),

    url(r'studies/create/$',
        staff_required_custom_login(survey_views.StudyCreate.as_view()),
        name='studies-create'),

    url(r'studies/$',
        staff_required_custom_login(survey_views.StudyList.as_view()),
        name='studies-list'),

    url(r'studies/deactivate/(?P<pk>[\w_\-]+)/$',
        staff_required_custom_login(survey_views.StudyDeactivate.as_view()),
        name='studies-deactivate'),

    url(r'studies/(?P<pk>[\w_\-]+)/$',
        staff_required_custom_login(survey_views.StudyDetail.as_view()),
        name='studies-detail'),

    url(r'surveys/edit/$',
        staff_required_custom_login(survey_views.SurveyListEdit.as_view()),
        name='surveys-list-edit'),

    url(r'surveys/run/$',
        login_required(survey_views.SurveyListRun.as_view()),
        name='surveys-list-run'),

    url(r'surveys/create/$',
        staff_required_custom_login(survey_views.SurveyCreate.as_view()),
        name='surveys-create'),

    # Create survey element
    url(_(r'^elements/create/(?P<form_entry_id>\d+)/'
          r'(?P<form_element_plugin_uid>[\w_\-]+)/$'),
        staff_required_custom_login(fobi.views.add_form_element_entry),
        name='fobi.add_form_element_entry'),

    # Edit survey element
    url(_(r'^elements/edit/(?P<form_element_entry_id>\d+)/$'),
        staff_required_custom_login(fobi.views.edit_form_element_entry),
        name='fobi.edit_form_element_entry'),

    # Delete survey element
    url(_(r'^elements/delete/(?P<form_element_entry_id>\d+)/$'),
        staff_required_custom_login(fobi.views.delete_form_element_entry),
        name='fobi.delete_form_element_entry'),

    # Create survey handler
    url(_(r'^handlers/create/(?P<form_entry_id>\d+)/'
          r'(?P<form_handler_plugin_uid>[\w_\-]+)/$'),
        view=staff_required_custom_login(fobi.views.add_form_handler_entry),
        name='fobi.add_form_handler_entry'),

    # Edit survey handler
    url(_(r'^handlers/edit/(?P<form_handler_entry_id>\d+)/$'),
        view=staff_required_custom_login(fobi.views.edit_form_handler_entry),
        name='fobi.edit_form_handler_entry'),

    # Delete survey handler
    url(_(r'^handlers/delete/(?P<form_handler_entry_id>\d+)/$'),
        view=staff_required_custom_login(fobi.views.delete_form_handler_entry),
        name='fobi.delete_form_handler_entry'),

    # Edit survey
    url(_(r'^surveys/edit/(?P<form_entry_id>\d+)/$'),
        staff_required_custom_login(fobi.views.edit_form_entry),
        name='fobi.edit_form_entry'),

    # Edit survey properties
    url(_(r'^surveys/edit/(?P<pk>\d+)/properties/$'),
        staff_required_custom_login(survey_views.SurveyPropertiesEdit.as_view()),
        name='survey-properties-edit'),

    # Delete survey
    url(_(r'^surveys/delete/(?P<form_entry_id>\d+)/$'),
        staff_required_custom_login(fobi.views.delete_form_entry),
        name='fobi.delete_form_entry'),

    # Deactivate survey
    url(_(r'^surveys/deactivate/(?P<pk>[\w_\-]+)/$'),
        staff_required_custom_login(survey_views.SurveyDeactivate.as_view()),
        name='surveys-deactivate'),

    # Publish survey
    url(_(r'^surveys/publish/(?P<form_entry_id>\d+)/$'),
        staff_required_custom_login(survey_views.SurveyPublish.as_view()),
        name='surveys-publish'),

    # Survey detail
    url(_(r'^surveys/view/(?P<form_entry_slug>[\w_\-]+)/$'),
        login_required(fobi.views.view_form_entry),
        name='fobi.view_form_entry'),

    # Submitted survey generic
    url(_(r'^surveys/view/submitted/$'),
        login_required(fobi.views.form_entry_submitted),
        name='fobi.form_entry_submitted'),

    # Submitted survey detail
    url(_(r'^surveys/view/(?P<form_entry_slug>[\w_\-]+)/submitted/$'),
        login_required(fobi.views.form_entry_submitted),
        name='fobi.form_entry_submitted'),

    # Export survey
    url(_(r'^surveys/export/(?P<form_entry_id>\d+)/$'),
        view=staff_required_custom_login(fobi.views.export_form_entry),
        name='fobi.export_form_entry'),

    # Import survey
    url(_(r'^surveys/import/$'),
        view=staff_required_custom_login(fobi.views.import_form_entry),
        name='fobi.import_form_entry'),

    # Survey importers
    url(_(r'^surveys/importer/(?P<form_importer_plugin_uid>[\w_\-]+)/$'),
        view=staff_required_custom_login(fobi.views.form_importer),
        name='fobi.form_importer'),

    # Delete form element entry
    url(_(r'^surveys/elements/delete/(?P<form_element_entry_id>\d+)/$'),
        staff_required_custom_login(fobi.views.delete_form_element_entry),
        name='fobi.delete_form_element_entry'),

    # Submitted surveys list
    url(r'^surveys/submitted$',
        staff_required_custom_login(survey_views.SurveySubmittedList.as_view()),
        name='surveys-submitted-list'),

    # Submitted surveys detail
    url(r'^surveys/submitted/(?P<form_entry_id>\d+)$',
        staff_required_custom_login(survey_views.SurveySubmittedDetail.as_view()),
        name='surveys-submitted-detail'),

    # API endpoint for retreiving CensusObservation data
    path('acs/', view=survey_views.census_area_to_observation, name="acs"),

    url(r'census-areas/region/$',
        staff_required_custom_login(survey_views.CensusAreaRegionSelect.as_view()),
        name='census-areas-region-select'),

    url(r'census-areas/create/$',
        staff_required_custom_login(survey_views.CensusAreaCreate.as_view()),
        name='census-areas-create'),

    url(r'census-areas/$',
        staff_required_custom_login(survey_views.CensusAreaList.as_view()),
        name='census-areas-list'),

    url(r'census-areas/edit/(?P<pk>\d+)/$',
        staff_required_custom_login(survey_views.CensusAreaEdit.as_view()),
        name='census-areas-edit'),

    url(r'census-areas/deactivate/(?P<pk>\d+)/$',
        staff_required_custom_login(survey_views.CensusAreaDeactivate.as_view()),
        name='census-areas-deactivate'),
]
