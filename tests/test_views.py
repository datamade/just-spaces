import uuid

import pytest
from django.urls import reverse
from pldp.forms import AGE_COMPLEX_CHOICES
from pldp.models import SurveyComponent

from surveys.models import CensusObservation
from fobi_custom.plugins.form_elements.fields import types as fobi_types


@pytest.mark.django_db
def test_home(client):
    url = reverse('home')
    get_response = client.get(url)

    assert get_response.status_code == 200


@pytest.mark.django_db
def test_study_area_create(client, user_staff):
    client.force_login(user_staff)
    url = reverse('study-areas-create')
    get_response = client.get(url)

    assert get_response.status_code == 200


@pytest.mark.django_db
def test_agency_create(client, user_staff):
    client.force_login(user_staff)
    url = reverse('agencies-create')
    response = client.get(url)

    assert response.status_code == 200


@pytest.mark.django_db
def test_agency_list(client, user_staff, agency):
    client.force_login(user_staff)
    url = reverse('agencies-list')
    response = client.get(url)

    agencies = response.context['agencies']
    active_agency = agencies[0]

    assert response.status_code == 200
    assert len(agencies) == 1
    assert active_agency.name == 'Sample Agency'


@pytest.mark.django_db
def test_agency_detail(client, user_staff, agency):
    client.force_login(user_staff)
    url = reverse('agencies-detail', kwargs={'pk': agency.id})
    response = client.get(url)
    html = response.content.decode('utf-8')

    assert response.status_code == 200

    for label, content in response.context['rows']:
        if content:
            assert label in html
            assert str(content) in html


@pytest.mark.django_db
def test_study_create(client, user_staff, study_area):
    client.force_login(user_staff)
    url = reverse('studies-create')
    response = client.get(url)

    assert response.status_code == 200
    assert study_area.name in response.content.decode('utf-8')
    assert response.context['form'].initial.get('agency') == user_staff.agency


@pytest.mark.django_db
def test_study_list(client, user_staff, study, study_inactive, study_agency_2):
    client.force_login(user_staff)
    url = reverse('studies-list')
    response = client.get(url)

    studies = response.context['studies']
    active_study = studies[0]

    assert response.status_code == 200
    assert len(studies) == 1
    assert active_study.title == 'Sample Study'


@pytest.mark.django_db
def test_study_detail(client, user_staff, study):
    client.force_login(user_staff)
    url = reverse('studies-detail', kwargs={'pk': study.id})
    response = client.get(url)
    html = response.content.decode('utf-8')

    assert response.status_code == 200

    for label, content in response.context['rows']:
        if content:
            assert label in html
            assert content in html


@pytest.mark.django_db
def test_location_create(client, user_staff):
    client.force_login(user_staff)
    url = reverse('locations-create')
    response = client.get(url)

    assert response.status_code == 200
    assert response.context['form'].initial.get('agency') == user_staff.agency


@pytest.mark.django_db
def test_location_list(client, user_staff, location, location_inactive, location_agency_2):
    client.force_login(user_staff)
    url = reverse('locations-list')
    response = client.get(url)

    locations = response.context['locations']
    active_location = locations[0]

    assert response.status_code == 200
    assert len(locations) == 1
    assert active_location.name_primary == 'Sample Location'


@pytest.mark.django_db
def test_location_detail(client, user_staff, location):
    client.force_login(user_staff)
    url = reverse('locations-detail', kwargs={'pk': location.id})
    response = client.get(url)
    html = response.content.decode('utf-8')

    assert response.status_code == 200

    for label, content in response.context['rows']:
        if content:
            assert label in html
            assert content in html


@pytest.mark.django_db
def test_survey_list_edit(client, user_staff, survey_form_entry,
                          survey_form_entry_inactive, survey_form_entry_observational,
                          survey_form_entry_agency_2):
    # Make sure that the SurveyFormEntry from Agency 2 is not published, to verify
    # that it doesn't get loaded on the Edit list view.
    survey_form_entry_agency_2.published = False
    survey_form_entry_agency_2.save()

    client.force_login(user_staff)
    url = reverse('surveys-list-edit')
    response = client.get(url)

    surveys = response.context['surveys']

    assert response.status_code == 200
    assert len(surveys) == 1


@pytest.mark.django_db
def test_survey_list_run(client, user_field, survey_form_entry,
                         survey_form_entry_inactive, survey_form_entry_observational,
                         survey_form_entry_agency_2):
    client.force_login(user_field)
    url = reverse('surveys-list-run')
    response = client.get(url)

    surveys = response.context['surveys']

    assert response.status_code == 200
    assert len(surveys) == 1


@pytest.mark.django_db
def test_survey_create(client, user_staff, study, study_agency_2):
    client.force_login(user_staff)
    url = reverse('surveys-create')
    response = client.get(url)

    # Make sure the user only sees Studies filtered by their agency, if one exists.
    form = response.context['form']
    available_studies = list(form.fields['study'].queryset)
    assert set(available_studies) == set([study])


@pytest.mark.django_db
def test_survey_edit_intercept(client, user_staff, survey_form_entry):
    client.force_login(user_staff)
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
def test_survey_edit_observational(client, user_staff, survey_form_entry_observational, form_element_observational):
    client.force_login(user_staff)
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
def test_survey_preview(client, user_staff, survey_form_entry_observational):
    client.force_login(user_staff)
    url = reverse('fobi.view_form_entry', kwargs={'form_entry_slug': survey_form_entry_observational.slug})
    response = client.get(url)

    assert response.status_code == 200
    assert not response.context['form_entry'].surveyformentry.published
    assert ('Preview ' + survey_form_entry_observational.name) in response.content.decode('utf-8')


@pytest.mark.django_db
def test_survey_run(client, user_field, survey_form_entry):
    client.force_login(user_field)
    url = reverse('fobi.view_form_entry', kwargs={'form_entry_slug': survey_form_entry.slug})
    response = client.get(url)

    assert response.status_code == 200
    assert response.context['form_entry'].surveyformentry.published
    assert (survey_form_entry.name) in response.content.decode('utf-8')


@pytest.mark.django_db
def test_survey_submitted_list(client, user_staff, survey, survey_form_entry,
                               survey_agency_2, survey_form_entry_agency_2):
    client.force_login(user_staff)
    url = reverse('surveys-submitted-list')
    response = client.get(url)

    surveys_submitted = response.context['surveys_submitted']

    assert response.status_code == 200
    assert len(surveys_submitted) == 1
    assert str(surveys_submitted.first().form_title) == 'Sample Form Entry'


@pytest.mark.django_db
def test_survey_submitted_detail(client, user_staff, survey_form_entry, survey, survey_row, survey_component):
    client.force_login(user_staff)

    url = reverse('surveys-submitted-detail', kwargs={'form_entry_id': survey_form_entry.id})
    response = client.get(url)

    surveys_submitted = response.context['surveys_submitted']

    assert response.status_code == 200
    assert len(surveys_submitted) == 1


@pytest.mark.django_db
def test_census_area_create(client, user_staff):
    client.force_login(user_staff)
    url = reverse('census-areas-create')
    response = client.get(url)

    assert response.status_code == 200
    assert response.context['form'].initial.get('agency') == user_staff.agency


@pytest.mark.django_db
def test_census_area_list(client, user_staff, census_area, census_area_agency_1,
                          census_area_agency_2):
    client.force_login(user_staff)
    url = reverse('census-areas-list')
    response = client.get(url)

    census_areas = response.context['census_areas']

    assert response.status_code == 200
    assert len(census_areas) == 2

    # Ensure that the only visible CensusAreas are A) those created by the agency
    # belonging to the user or B) those where CensusArea.agency is null
    for area in census_areas:
        assert area.name in [area.name for area in (census_area, census_area_agency_1)]


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
