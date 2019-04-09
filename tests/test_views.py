import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_survey_submitted_list(client, user, survey, form_entry):
    client.force_login(user)
    url = reverse('surveys-submitted-list')
    response = client.get(url)

    surveys_submitted = response.context['surveys_submitted']

    assert response.status_code == 200
    assert len(surveys_submitted) == 1
    assert str(surveys_submitted.first().form_title) == 'Sample Form Entry'


@pytest.mark.django_db
def test_survey_submitted_detail(client, user, form_entry, survey, survey_row, survey_component):
    client.force_login(user)
    url = reverse('surveys-submitted-detail', kwargs={'form_entry_id': form_entry.id})
    response = client.get(url)

    surveys_submitted = response.context['surveys_submitted']

    assert response.status_code == 200
    assert len(surveys_submitted) == 1
