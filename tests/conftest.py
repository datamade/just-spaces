import pytest

from fobi.models import FormEntry
from surveys.models import JustSpacesUser
from pldp.models import Location, Agency, Study, StudyArea

@pytest.fixture
@pytest.mark.django_db
def sample_user(db):
    sample_user = JustSpacesUser.objects.create(
        username='testuser'
    )
    sample_user.save()

    return sample_user


@pytest.fixture
@pytest.mark.django_db
def sample_agency(db):
    sample_agency = Agency.objects.create(

    )
    sample_agency.save()

    return sample_agency


@pytest.fixture
@pytest.mark.django_db
def sample_study_area(db):
    sample_study_area = StudyArea.objects.create(

    )
    sample_study_area.save()

    return sample_study_area


@pytest.fixture
@pytest.mark.django_db
def sample_study(db):
    sample_study = Study.objects.create(

    )
    sample_study.save()

    return sample_study

def sample_location(db):
    sample_location = Location.objects.create(

    )
    sample_location.save()

    return sample_location

@pytest.fixture
@pytest.mark.django_db
def form_entry(db, sample_user):
    # Fixtures provide context for tests.
    # Testing the CollectDataPlugin requires an instance of a FormEntry
    # https://github.com/barseghyanartur/django-fobi/blob/070ee3239cc4df3f5e841ee8649d8c26a10f007e/src/fobi/models.py#L363

    # An example of a simple fixture:
    # https://github.com/datamade/la-metro-councilmatic/blob/master/tests/conftest.py#L47

    form_entry_info = {
        'user' : sample_user,
        'name' : 'Test Form Entry',
    }

    form_entry = FormEntry.objects.create(**form_entry_info)
    form_entry.save()

    return form_entry
