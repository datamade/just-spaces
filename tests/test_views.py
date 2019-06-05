import uuid

import pytest
from django.urls import reverse
from pldp.forms import AGE_COMPLEX_CHOICES
from pldp.models import SurveyComponent

from surveys.models import CensusObservation
from fobi_custom.plugins.form_elements.fields import types as fobi_types


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
def test_location_create(client, user):
    client.force_login(user)
    url = reverse('locations-create')
    response = client.get(url)

    assert response.status_code == 200


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
                         'household_tenure', 'What year did you move into your current address?'),
                         ('own_or_rent', 'Are you a homeowner or a renter?'),
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


@pytest.mark.django_db
def test_census_area_to_observation(client, census_area, survey_row):
    """
    Test that the census_area_to_observation API endpoint returns the correct
    set of CensusObservations for a given CensusArea and SurveyComponent.
    """
    survey_component = SurveyComponent.objects.create(
        detail_level='basic',
        name=str(uuid.uuid4()),
        label='Age',
        type='age_intercept',
        position=2,
        saved_data=10,
        row=survey_row,
    )
    census_observation = CensusObservation.objects.create(
        fips_code=census_area.fips_codes[0],
        variable=fobi_types.TYPES_TO_ACS_VARIABLES['age_intercept']['basic'],
        fields={'0-4': 0, '5-14': 1, '15-24': 3, '25-44': 5, '45-64': 0, '65-74': 12, '75+': 0},
    )
    response = client.get(
        reverse('acs'),
        {'census_area': census_area.id, 'primary_source': survey_component.name}
    )
    assert response.status_code == 200
    assert response.json().get('data') is not None
    assert response.json()['data'] == census_observation.fields


def test_census_area_to_observation_no_kwargs(client):
    """
    Test that the census_area_to_observation API endpoint will raise an error if
    it's missing the required keyword arguments.
    """
    response = client.get(reverse('acs'))
    assert response.status_code == 400
    assert response.json().get('error') is not None
    assert 'required query parameters' in response.json()['error']


@pytest.mark.django_db
def test_census_area_to_observation_no_census_area(client):
    """
    Test that the census_area_to_observation API endpoint will raise an error if
    no CensusArea object matches the census_area parameter.
    """
    response = client.get(
        reverse('acs'),
        {'census_area': '10000', 'primary_source': 'bar'}
    )
    assert response.status_code == 400
    assert response.json().get('error') is not None
    assert 'No CensusArea object' in response.json()['error']


@pytest.mark.django_db
def test_census_area_to_observation_no_survey_component(client, census_area):
    """
    Test that the census_area_to_observation API endpoint will raise an error if
    no SurveyComponent matches the given value for primary_source.
    """
    response = client.get(
        reverse('acs'),
        {'census_area': census_area.id, 'primary_source': 'bar'}
    )
    assert response.status_code == 400
    assert response.json().get('error') is not None
    assert 'No SurveyComponent found' in response.json()['error']


@pytest.mark.django_db
def test_census_area_to_observation_no_acs_variable(client, census_area, survey_component):
    """
    Test that the census_area_to_observation API endpoint will raise an error if
    the SurveyComponent in question does not have a matching ACS variable.
    """
    response = client.get(
        reverse('acs'),
        {'census_area': census_area.id, 'primary_source': survey_component.name}
    )
    assert response.status_code == 400
    assert response.json().get('error') is not None
    assert 'No corresponding ACS variable' in response.json()['error']
