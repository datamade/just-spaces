import pytest
from django.urls import reverse

from pldp.models import StudyArea


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
