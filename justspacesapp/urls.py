"""justspaces URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _
from justspacesapp.views import CreateAgency, CreateLocation, CreateStudy, \
                                EditSurvey, RunSurvey
import fobi.views

urlpatterns = [
    url(r'^$',
        RunSurvey.as_view(),
        name='home'),

    url(r'agencies/create$',
        CreateAgency.as_view(),
        name='agencies-create'),

    url(r'locations/create$',
        CreateLocation.as_view(),
        name='locations-create'),

    url(r'studies/create$',
        CreateStudy.as_view(),
        name='studies-create'),

    # Create new survey
    url(r'surveys/create$',
        view=fobi.views.create_form_entry,
        name='fobi.create_form_entry'),

    # Create survey element
    url(_(r'^surveys/elements/create/(?P<form_entry_id>\d+)/'
          r'(?P<form_element_plugin_uid>[\w_\-]+)/$'),
        view=fobi.views.add_form_element_entry,
        name='fobi.add_form_element_entry'),

    # Edit survey element
    url(_(r'^surveys/elements/edit/(?P<form_element_entry_id>\d+)/$'),
        view=fobi.views.edit_form_element_entry,
        name='fobi.edit_form_element_entry'),

    # Delete survey element
    url(_(r'^surveys/elements/delete/(?P<form_element_entry_id>\d+)/$'),
        view=fobi.views.delete_form_element_entry,
        name='fobi.delete_form_element_entry'),

    # Create survey handler
    url(_(r'^surveys/handlers/create/(?P<form_entry_id>\d+)/'
          r'(?P<form_handler_plugin_uid>[\w_\-]+)/$'),
        view=fobi.views.add_form_handler_entry,
        name='fobi.add_form_handler_entry'),

    # Edit survey handler
    url(_(r'^surveys/handlers/edit/(?P<form_handler_entry_id>\d+)/$'),
        view=fobi.views.edit_form_handler_entry,
        name='fobi.edit_form_handler_entry'),

    # Delete survey handler
    url(_(r'^surveys/handlers/delete/(?P<form_handler_entry_id>\d+)/$'),
        view=fobi.views.delete_form_handler_entry,
        name='fobi.delete_form_handler_entry'),

    # Edit survey
    url(_(r'^surveys/edit/(?P<form_entry_id>\d+)/$'),
        view=fobi.views.edit_form_entry,
        name='fobi.edit_form_entry'),

    # Delete survey
    url(_(r'^surveys/delete/(?P<form_entry_id>\d+)/$'),
        view=fobi.views.delete_form_entry,
        name='delete_form_entry'),

    # Survey list edit
    url(r'surveys/edit$',
        EditSurvey.as_view(),
        name='survey-list-edit'),

    # Survey list view
    url(r'surveys/view$',
        RunSurvey.as_view(),
        name='survey-list-view'),

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
]
