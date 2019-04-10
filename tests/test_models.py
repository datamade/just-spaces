import pytest

from users.models import JustSpacesUser


@pytest.mark.django_db
def test_user(user):
    saved_user = JustSpacesUser.objects.first()

    assert saved_user.agency.name == 'Sample Agency'

# def test_survey_form_entry():
#
