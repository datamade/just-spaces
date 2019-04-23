import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_survey_list_edit(client, user, survey_form_entry, survey_form_entry_observational):
    client.force_login(user)
    url = reverse('surveys-list-edit')
    response = client.get(url)

    surveys = response.context['surveys']

    assert response.status_code == 200
    assert len(surveys) == 1


@pytest.mark.django_db
def test_survey_list_run(client, user, survey_form_entry, survey_form_entry_observational):
    client.force_login(user)
    url = reverse('surveys-list-run')
    response = client.get(url)

    surveys = response.context['surveys']

    assert response.status_code == 200
    assert len(surveys) == 1


@pytest.mark.django_db
def test_survey_edit_intercept(client, user, survey_form_entry):
    client.force_login(user)
    url = reverse('fobi.edit_form_entry', kwargs={'form_entry_id': survey_form_entry.id})
    response = client.get(url)

    plugins = response.context['user_form_element_plugins']

    assert response.status_code == 200
    assert len(plugins) == 3


@pytest.mark.django_db
def test_survey_edit_observational(client, user, survey_form_entry_observational):
    client.force_login(user)
    url = reverse('fobi.edit_form_entry', kwargs={'form_entry_id': survey_form_entry_observational.id})
    response = client.get(url)

    plugins = response.context['user_form_element_plugins']

    assert response.status_code == 200
    assert len(plugins) == 4


@pytest.mark.django_db
def test_survey_preview(client, user, survey_form_entry_observational):
    client.force_login(user)
    url = reverse('fobi.view_form_entry', kwargs={'form_entry_slug': survey_form_entry_observational.slug})
    response = client.get(url)

    print('Preview ' + survey_form_entry_observational.name)
    print(response.content.decode('utf-8'))

    assert response.status_code == 200
    assert not response.context['form_entry'].surveyformentry.published
    assert ('Preview ' + survey_form_entry_observational.name) in response.content.decode('utf-8')


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
