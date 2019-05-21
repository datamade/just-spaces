import pytest
from datetime import datetime
from django.core.management import call_command
from django.utils.timezone import get_current_timezone

from fobi.models import FormElementEntry
from users.models import JustSpacesUser
from surveys.models import SurveyFormEntry
from pldp.models import Location, Agency, Study, StudyArea, Survey, \
                        SurveyRow, SurveyComponent


@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command('initialize_pldp')


@pytest.fixture
@pytest.mark.django_db
def agency(db):
    agency = Agency.objects.create(
        name='Sample Agency',
        email='test@email.com',
        type='educational institute',
        language_id='en',
    )

    return agency


@pytest.fixture
@pytest.mark.django_db
def user(db, agency):
    user = JustSpacesUser.objects.create(
        username='sampleuser',
        agency=agency,
        is_superuser=True
    )

    return user


@pytest.fixture
@pytest.mark.django_db
def study_area(db):
    study_area = StudyArea.objects.create(
        name='Sample Study Area',
        area='POLYGON((-101.744384 39.32155, -101.552124 39.330048, -101.403808 39.330048, -101.332397 39.364032, -101.744384 39.32155))',
    )
    study_area.save()

    return study_area


@pytest.fixture
@pytest.mark.django_db
def study(db, agency):
    study = Study.objects.create(
        title='Sample Study',
        manager_name='Sample Study Manager',
        agency=agency
    )

    return study


@pytest.fixture
@pytest.mark.django_db
def location(db, agency):
    location = Location.objects.create(
        name_primary='Sample Location',
        agency=agency,
        country_id='US',
        geometry='POLYGON((-101.744384 39.32155, -101.552124 39.330048, -101.403808 39.330048, -101.332397 39.364032, -101.744384 39.32155))',
    )

    return location


@pytest.fixture
@pytest.mark.django_db
def survey_form_entry(db, user, location, study):
    survey_form_entry_info = {
        'id': 1,
        'user': user,
        'name': 'Sample Form Entry',
        'published': True,
        'location': location,
        'study': study,
        'type': 'intercept',
    }

    survey_form_entry = SurveyFormEntry.objects.create(**survey_form_entry_info)

    return survey_form_entry


@pytest.fixture
@pytest.mark.django_db
def survey_form_entry_observational(db, user, location, study):
    survey_form_entry_observational_info = {
        'id': 2,
        'user': user,
        'name': 'Sample Form Entry Observational',
        'published': False,
        'location': location,
        'study': study,
        'type': 'observational',
    }

    survey_form_entry_observational = SurveyFormEntry.objects.create(**survey_form_entry_observational_info)

    return survey_form_entry_observational


@pytest.fixture
@pytest.mark.django_db
def form_element_float(db, survey_form_entry):
    form_element_info = {
        'plugin_data': '{"label": "Sample Float Field", "help_text": " ", \
            "max_value": null, "name": "c75e27cf-4d8f-49dc-bb15-da8137dac247", \
            "required": false, "min_value": null, "initial": null}',
        'plugin_uid': 'float',
        'position': 2,
        'form_entry': survey_form_entry,

    }

    form_element = FormElementEntry.objects.create(
        **form_element_info
    )

    return form_element


@pytest.fixture
@pytest.mark.django_db
def form_element_help_text(db, survey_form_entry):
    form_element_help_text_info = {
        'plugin_data': '{"text": "This survey will take 3-4 minutes."}',
        'plugin_uid': 'content_text',
        'position': 1,
        'form_entry': survey_form_entry,

    }

    form_element_help_text = FormElementEntry.objects.create(
        **form_element_help_text_info
    )

    return form_element_help_text


@pytest.fixture
@pytest.mark.django_db
def form_element_time_start(db, survey_form_entry):
    form_element_time_start_info = {
        'plugin_data': '{"label": "What is the stop time of this survey?", "name": "c14d02bc-312f-44a5-843f-cc45baa79dc3", "help_text": "", "required": false}',
        'plugin_uid': 'time_start',
        'position': 3,
        'form_entry': survey_form_entry,

    }

    form_element_time_start = FormElementEntry.objects.create(
        **form_element_time_start_info
    )

    return form_element_time_start


@pytest.fixture
@pytest.mark.django_db
def form_element_observational(db, survey_form_entry_observational):
    form_element_observational_info = {
        'plugin_data': '{"label": "How many people do you see in each age \
                        range?", "name": "57bc76ce-c8dc-4d64-acd6-955d455fac20", \
                        "detail_level": "complex", "help_text": "", "required": false}',
        'plugin_uid': 'age_observational',
        'position': 1,
        'form_entry': survey_form_entry_observational,

    }

    form_element_observational = FormElementEntry.objects.create(
        **form_element_observational_info
    )

    return form_element_observational


@pytest.fixture
@pytest.mark.django_db
def survey(db, location, study):
    survey = Survey.objects.create(
        time_stop=datetime.now(tz=get_current_timezone()),
        location=location,
        study=study,
        form_id=1,
    )

    return survey


@pytest.fixture
@pytest.mark.django_db
def survey_row(db, survey):
    survey_row = SurveyRow.objects.create(
        survey=survey,
    )

    return survey_row


@pytest.fixture
@pytest.mark.django_db
def survey_component(db, survey_row):
    survey_component = SurveyComponent.objects.create(
        detail_level='basic',
        name='8e5a7a02-0e39-4a21-b8f9-710728bf7a70',
        label='Test label',
        type='float',
        position=1,
        saved_data=10,
        row=survey_row,
    )

    return survey_component
