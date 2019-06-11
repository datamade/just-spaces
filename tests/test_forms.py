import pytest
from django.urls import reverse

from pldp.models import StudyArea, Location, LocationLine
from surveys.models import SurveyFormEntry


@pytest.mark.django_db
def test_study_area_form(client, user):
    client.force_login(user)
    url = reverse('study-areas-create')

    form_data = {
        'name': 'New Study Area',
        'area': '{"type":"Polygon","coordinates":[[[-75.213295,39.941767],\
            [-75.213295,39.962624],[-75.148938,39.962624],\
            [-75.148938,39.941767],[-75.213295,39.941767]]]}',
    }

    post_response = client.post(url, form_data)
    new_study_area = StudyArea.objects.first()

    assert post_response.status_code == 302
    assert new_study_area.name == form_data['name']
    assert new_study_area.area


@pytest.mark.django_db
def test_study_deactivate(client, user, study):
    client.force_login(user)
    assert study.is_active

    url = reverse('studies-deactivate', kwargs={'pk': study.id})

    get_response = client.get(url)

    assert get_response.status_code == 200

    post_response = client.post(url)
    study.refresh_from_db()

    assert post_response.status_code == 302
    assert not study.is_active


@pytest.mark.django_db
def test_location_form(client, user, agency):
    client.force_login(user)
    url = reverse('locations-create')

    form_data = {
        'location-agency': agency.id,
        'location-country': 'US',
        'location-name_primary': 'New Location',
        'location-geometry': ['{"type":"LineString","coordinates":[[-75.205911,39.934886],[-75.138839,39.952281]]}'],
        'location-geometry_type': 'line',
        'location-area-date_measured': ['2019-05-20'],
        'location-line-date_measured': ['2019-05-21'],
    }

    post_response = client.post(url, form_data)
    new_location = Location.objects.first()
    new_location_line = LocationLine.objects.first()

    assert post_response.status_code == 302
    assert new_location.name_primary == form_data['location-name_primary']
    assert new_location_line.location == new_location


@pytest.mark.django_db
def test_location_deactivate(client, user, location):
    client.force_login(user)
    assert location.is_active

    url = reverse('locations-deactivate', kwargs={'pk': location.id})

    get_response = client.get(url)

    assert get_response.status_code == 200

    post_response = client.post(url)
    location.refresh_from_db()

    assert post_response.status_code == 302
    assert not location.is_active


@pytest.mark.django_db
def test_survey_form(client, user, study, location):
    client.force_login(user)
    url = reverse('surveys-create')
    get_response = client.get(url)

    form_data = {
        'user': get_response.context['form']['user'].value(),
        'name': 'Test Survey',
        'study': study.id,
        'location': location.id,
        'type': get_response.context['form']['type'].value(),
    }

    post_response = client.post(url, form_data)
    new_survey_form = SurveyFormEntry.objects.get(name='Test Survey')

    assert post_response.status_code == 302
    assert new_survey_form.user == user
    assert new_survey_form.study == study
    assert new_survey_form.location == location
    assert new_survey_form.type == 'intercept'


@pytest.mark.django_db
def test_survey_deactivate(client, user, survey_form_entry):
    client.force_login(user)
    assert survey_form_entry.active

    url = reverse('surveys-deactivate', kwargs={'pk': survey_form_entry.id})

    get_response = client.get(url)

    assert get_response.status_code == 200

    post_response = client.post(url)
    survey_form_entry.refresh_from_db()

    assert post_response.status_code == 302
    assert not survey_form_entry.active


@pytest.mark.django_db
def test_survey_publish(client, survey_form_entry_observational):
    assert not survey_form_entry_observational.published

    url = reverse('surveys-publish', kwargs={'form_entry_id': survey_form_entry_observational.id})

    get_response = client.get(url)

    assert get_response.status_code == 200

    post_response = client.post(url)
    survey_form_entry_observational.refresh_from_db()

    assert post_response.status_code == 302
    assert survey_form_entry_observational.published
