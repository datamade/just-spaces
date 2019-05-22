import pytest
from django.urls import reverse

from pldp.models import StudyArea, Location, LocationLine


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
def test_location_form(client, user, agency):
    client.force_login(user)
    url = reverse('locations-create')

    form_data = {'location-agency': agency.id,
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
