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
from django.conf.urls import url, include
from justspacesapp.views import CreateAgency, CreateLocation, CreateStudy, \
                                EditSurvey, RunSurvey
from fobi.views import create_form_entry

urlpatterns = [
    url(r'^$', RunSurvey.as_view(), name='home'),
    url(r'create-agency$', CreateAgency.as_view(), name='create-agency'),
    url(r'create-location$', CreateLocation.as_view(), name='create-location'),
    url(r'create-study$', CreateStudy.as_view(), name='create-study'),
    url(r'create-survey$', view=create_form_entry, name='fobi.create_form_entry'),
    url(r'edit-survey$', EditSurvey.as_view(), name='edit-survey'),
    url(r'run-survey$', RunSurvey.as_view(), name='run-survey'),
]
