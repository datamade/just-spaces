from django.views.generic import ListView, TemplateView
from django.views.generic.edit import CreateView, FormView
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate

from pldp.models import Agency, Location, Study
from fobi.models import FormEntry

from .models import JustSpacesUser
from .admin import JustSpacesUserCreationForm


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
    model = Study
    template_name = "study_create.html"
    fields = '__all__'
    success_url = '/'


class SurveyList(ListView):
    model = FormEntry
    template_name = "survey_list.html"
    context_object_name = 'surveys'

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
