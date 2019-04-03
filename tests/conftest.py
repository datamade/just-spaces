import pytest
from django.core.management import call_command

from fobi.models import FormEntry, FormElementEntry
from surveys.models import JustSpacesUser
from pldp.models import Location, Agency, Study, StudyArea


@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command('initialize_pldp')


@pytest.fixture
@pytest.mark.django_db
def user(db):
    user = JustSpacesUser.objects.create(
        username='sampleuser'
    )

    return user


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
        primary_name='Sample Location',
        agency=agency,
        country_id='US',
    )

    return location


@pytest.fixture
@pytest.mark.django_db
def form_entry(db, user):
    form_entry_info = {
        'user': user,
        'name': 'Sample Form Entry',
    }

    form_entry = FormEntry.objects.create(**form_entry_info)

    return form_entry


@pytest.fixture
@pytest.mark.django_db
def form_element(db, form_entry):
    form_element_info = {
        'plugin_data': '{"label": "Sample Float Field", "help_text": " ", \
            "max_value": null, "name": "c75e27cf-4d8f-49dc-bb15-da8137dac247", \
            "required": false, "min_value": null, "initial": null}',
        'plugin_uid': 'float',
        'position': 1,
        'form_entry': form_entry,

    }

    form_element = FormElementEntry.objects.create(
        **form_element_info
    )

    return form_element
