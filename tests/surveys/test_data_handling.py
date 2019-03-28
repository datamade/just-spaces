import pytest
import requests

from fobi_custom.plugins.form_handlers.collect_data.fobi_form_handlers import CollectDataPlugin
from fobi.dynamic import assemble_form_class

# pass in your fixture (from conftest.py)
# pass in mocker the fixture (from https://github.com/pytest-dev/pytest-mock/)
def test_handler(form_entry, mocker):
    # https://github.com/barseghyanartur/django-fobi/blob/070ee3239cc4df3f5e841ee8649d8c26a10f007e/src/fobi/dynamic.py#L126
    form = assemble_form_class(form_entry=form_entry)
    request = mocker.MagicMock(spec=requests.Response)

    # A valid CollectDataPlugin requires a DynamicForm, a FormEntry, and a post request.
    plugin = CollectDataPlugin()
    plugin.run(form=form,
               form_entry=form_entry,
               request=request)

    assert True == True
