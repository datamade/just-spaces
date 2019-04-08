"""justspaces URL Configuration

Many of the following views are taken from django-fobi, and follow their
naming url patterns. As this app grows in complexity, we may want to
refigure it to a more strictful RESTful approach.

"""
from django.conf.urls import url, include
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.decorators import login_required, permission_required
from surveys.views import AgencyCreate, LocationCreate, StudyCreate, \
                                SurveyList, Signup, CollectedDataList
import fobi.views

from fobi.contrib.plugins.form_handlers.db_store.views import \
                                       view_saved_form_data_entries, \
                                       export_saved_form_data_entries

urlpatterns = [
    # placeholder view for a public-facing landing page
    url(r'^$',
        login_required(SurveyList.as_view()),
        name='home'),

    url(r'^accounts/',
        include('django.contrib.auth.urls')),

    url(r'^accounts/signup$',
        Signup.as_view(),
        name='signup'),


    url(r'agencies/create/$',
        login_required(AgencyCreate.as_view()),
        name='agencies-create'),

    url(r'locations/create/$',
        login_required(LocationCreate.as_view()),
        name='locations-create'),

    url(r'studies/create/$',
        login_required(StudyCreate.as_view()),
        name='studies-create'),

    # Survey list
    url(r'surveys/$',
        login_required(SurveyList.as_view()),
        name='survey-list'),

    # Create new survey
    url(r'surveys/create/$',
        view=fobi.views.create_form_entry,
        name='fobi.create_form_entry'),

    # Create survey element
    url(_(r'^elements/create/(?P<form_entry_id>\d+)/'
          r'(?P<form_element_plugin_uid>[\w_\-]+)/$'),
        view=fobi.views.add_form_element_entry,
        name='fobi.add_form_element_entry'),

    # Edit survey element
    url(_(r'^elements/edit/(?P<form_element_entry_id>\d+)/$'),
        view=fobi.views.edit_form_element_entry,
        name='fobi.edit_form_element_entry'),

    # Delete survey element
    url(_(r'^elements/delete/(?P<form_element_entry_id>\d+)/$'),
        view=fobi.views.delete_form_element_entry,
        name='fobi.delete_form_element_entry'),

    # Create survey handler
    url(_(r'^handlers/create/(?P<form_entry_id>\d+)/'
          r'(?P<form_handler_plugin_uid>[\w_\-]+)/$'),
        view=fobi.views.add_form_handler_entry,
        name='fobi.add_form_handler_entry'),

    # Edit survey handler
    url(_(r'^handlers/edit/(?P<form_handler_entry_id>\d+)/$'),
        view=fobi.views.edit_form_handler_entry,
        name='fobi.edit_form_handler_entry'),

    # Delete survey handler
    url(_(r'^handlers/delete/(?P<form_handler_entry_id>\d+)/$'),
        view=fobi.views.delete_form_handler_entry,
        name='fobi.delete_form_handler_entry'),

    # Edit survey
    url(_(r'^surveys/edit/(?P<form_entry_id>\d+)/$'),
        view=fobi.views.edit_form_entry,
        name='fobi.edit_form_entry'),

    # Delete survey
    url(_(r'^surveys/delete/(?P<form_entry_id>\d+)/$'),
        view=fobi.views.delete_form_entry,
        name='fobi.delete_form_entry'),

    # Survey detail
    url(_(r'^surveys/view/(?P<form_entry_slug>[\w_\-]+)/$'),
        view=fobi.views.view_form_entry,
        name='fobi.view_form_entry'),

    # Submitted survey generic
    url(_(r'^surveys/view/submitted/$'),
        view=fobi.views.form_entry_submitted,
        name='fobi.form_entry_submitted'),

    # Submitted survey detail
    url(_(r'^surveys/view/(?P<form_entry_slug>[\w_\-]+)/submitted/$'),
        view=fobi.views.form_entry_submitted,
        name='fobi.form_entry_submitted'),

    # Export survey
    url(_(r'^surveys/export/(?P<form_entry_id>\d+)/$'),
        view=fobi.views.export_form_entry,
        name='fobi.export_form_entry'),

    # Import survey
    url(_(r'^surveys/import/$'),
        view=fobi.views.import_form_entry,
        name='fobi.import_form_entry'),

    # Survey importers
    url(_(r'^surveys/importer/(?P<form_importer_plugin_uid>[\w_\-]+)/$'),
        view=fobi.views.form_importer,
        name='fobi.form_importer'),

    # Delete form element entry
    url(_(r'^surveys/elements/delete/(?P<form_element_entry_id>\d+)/$'),
        view=fobi.views.delete_form_element_entry,
        name='fobi.delete_form_element_entry'),

    # Submitted data list
    url(r'^collected-data/$',
        view=CollectedDataList.as_view(),
        name='collected-data-list'),
]
