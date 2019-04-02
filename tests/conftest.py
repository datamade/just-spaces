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
def sample_user(db):
    sample_user = JustSpacesUser.objects.create(
        username='sampleuser'
    )
    sample_user.save()

    return sample_user


@pytest.fixture
@pytest.mark.django_db
def sample_agency(db):
    sample_agency = Agency.objects.create(
        name='Sample Agency',
        email='test@email.com',
        type='educational institute',
        language_id='en',
    )
    sample_agency.save()

    return sample_agency


# @pytest.fixture
# @pytest.mark.django_db
# def sample_study_area(db):
#     sample_study_area = StudyArea.objects.create(
#
#     )
#     sample_study_area.save()
#
#     return sample_study_area


@pytest.fixture
@pytest.mark.django_db
def sample_study(db, sample_agency):
    sample_study = Study.objects.create(
        title='Sample Study',
        manager_name='Sample Study Manager',
        agency=Agency.objects.get(name='Sample Agency')
    )
    sample_study.save()

    return sample_study


@pytest.fixture
@pytest.mark.django_db
def sample_location(db, sample_agency):
    sample_location = Location.objects.create(
        primary_name='Sample Location',
        agency=Agency.objects.get(name='Sample Agency'),
        country_id='US',
    )
    sample_location.save()

    return sample_location


@pytest.fixture
@pytest.mark.django_db
def sample_form_entry(db, sample_user):
    sample_form_entry_info = {
        'user' : sample_user,
        'name' : 'Sample Form Entry',
    }

    sample_form_entry = FormEntry.objects.create(**sample_form_entry_info)
    sample_form_entry.save()

    return sample_form_entry


@pytest.fixture
@pytest.mark.django_db
def sample_form_element(db, sample_form_entry):
    sample_form_element_info = {
        'plugin_data' : '{"label": "Sample Float Field", "help_text": " ", "max_value": null, "name": "c75e27cf-4d8f-49dc-bb15-da8137dac247", "required": false, "min_value": null, "initial": null}',
        'plugin_uid' : 'float',
        'position' : 1,
        'form_entry' : sample_form_entry,

    }

    sample_form_element = FormElementEntry.objects.create(
        **sample_form_element_info
    )
    sample_form_element.save()

    return sample_form_element
