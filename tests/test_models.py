import pytest

from users.models import JustSpacesUser
from surveys.models import SurveyFormEntry


@pytest.mark.django_db
def test_user(user):
    saved_user = JustSpacesUser.objects.first()

    assert saved_user.agency.name == 'Sample Agency'


@pytest.mark.django_db
def test_survey_form_entry(client, user, survey_form_entry):
    saved_survey_form_entry = SurveyFormEntry.objects.first()

    assert saved_survey_form_entry.name == 'Sample Form Entry'
    assert saved_survey_form_entry.published
    assert saved_survey_form_entry.type == 'intercept'
