import pytest

from fobi.models import FormEntry

@pytest.fixture
@pytest.mark.django_db
def form_entry(db):
    # Fixtures provide context for your tests.
    # Testing the CollectDataPlugin requires an instance of a FormEntry
    # https://github.com/barseghyanartur/django-fobi/blob/070ee3239cc4df3f5e841ee8649d8c26a10f007e/src/fobi/models.py#L363

    # Here's an example of how to do create a simple fixture: https://github.com/datamade/la-metro-councilmatic/blob/master/tests/conftest.py#L47
