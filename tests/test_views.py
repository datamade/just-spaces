import pytest
from django.urls import reverse

from pldp.forms import AGE_COMPLEX_CHOICES

@pytest.mark.django_db
def test_study_area_create(client, user):
    client.force_login(user)
    url = reverse('study-areas-create')
    get_response = client.get(url)

    assert get_response.status_code == 200


@pytest.mark.django_db
def test_study_create(client, user, study_area):
    client.force_login(user)
    url = reverse('studies-create')
    response = client.get(url)

    assert response.status_code == 200
    assert study_area.name in response.content.decode('utf-8')


@pytest.mark.django_db
def test_survey_list_edit(client, user, survey_form_entry, survey_form_entry_observational):
    client.force_login(user)
    url = reverse('surveys-list-edit')
    response = client.get(url)

    surveys = response.context['surveys']

    assert response.status_code == 200
    assert len(surveys) == 1


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

    intercept_presets = [('age_intercept', 'How old are you?'),
                         ('education', 'What is your highest formal degree of education?'),
                         ('employment', 'What is your current employment status?'),
                         ('gender_intercept', 'What gender do you most identify with?'), (
                         'household_tenure', 'How many years have you lived at your current address?'),
                         ('income', 'Are you a homeowner or a renter?'),
                         ('race', 'Which race or ethnicity best describes you?'),
                         ('transportation', 'How did you travel here?')]

    assert response.status_code == 200
    assert len(plugins) == 4

    for question in intercept_presets:
        assert question in plugins['Intercept']


@pytest.mark.django_db
def test_survey_edit_observational(client, user, survey_form_entry_observational, form_element_observational):
    client.force_login(user)
    url = reverse('fobi.edit_form_entry', kwargs={'form_entry_id': survey_form_entry_observational.id})
    response = client.get(url)

    plugins = response.context['user_form_element_plugins']
    html = response.content.decode('utf-8')

    assert response.status_code == 200
    assert len(plugins) == 4

    for choice, _ in AGE_COMPLEX_CHOICES:
        label = '<label>{}</label>'.format(choice)
        assert label in html


@pytest.mark.django_db
def test_survey_preview(client, user, survey_form_entry_observational):
    client.force_login(user)
    url = reverse('fobi.view_form_entry', kwargs={'form_entry_slug': survey_form_entry_observational.slug})
    response = client.get(url)

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
