import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_survey_list_run(client, user, survey_form_entry):
    client.force_login(user)
    url = reverse('surveys-list')
    url += '?published=f'
    response = client.get(url)

    surveys = response.context['surveys']

    assert response.status_code == 200
    assert len(surveys) == 1


@pytest.mark.django_db
def test_survey_publish(client, survey_form_entry):
    assert not survey_form_entry.published

    url = reverse('surveys-publish', kwargs={'form_entry_id': survey_form_entry.id})

    get_response = client.get(url)

    assert get_response.status_code == 200

    post_response = client.post(url)
    survey_form_entry.refresh_from_db()

    assert post_response.status_code == 302
    assert survey_form_entry.published


@pytest.mark.django_db
def test_survey_submitted_list(client, user, survey, survey_form_entry):
    client.force_login(user)
    url = reverse('surveys-submitted-list')
    response = client.get(url)

    surveys_submitted = response.context['surveys_submitted']

    assert response.status_code == 200
    assert len(surveys_submitted) == 1
    assert str(surveys_submitted.first().form_title) == 'Sample Form Entry'


@pytest.mark.django_db
def test_survey_submitted_detail(client, user, survey_form_entry, survey, survey_row, survey_component):
    client.force_login(user)

    url = reverse('surveys-submitted-detail', kwargs={'form_entry_id': survey_form_entry.id})
    response = client.get(url)

    surveys_submitted = response.context['surveys_submitted']

    assert response.status_code == 200
    assert len(surveys_submitted) == 1
