import pytest
import requests

from django.core.management import call_command

from fobi_custom.plugins.form_handlers.collect_data.fobi_form_handlers import CollectDataPlugin
from fobi.dynamic import assemble_form_class

from pldp.models import Survey

# pass in form_entry fixture from conftest.py and mocker fixture
def test_handler(form_entry, mocker):

    # load languages and countries from the pldp
    call_command('initialize_pldp')

    # load sample pldp models: Sample Study, Sample Agency, Sample Location, etc
    call_command('loaddata', 'pldp_sample.json')

    # https://github.com/barseghyanartur/django-fobi/blob/070ee3239cc4df3f5e841ee8649d8c26a10f007e/src/fobi/dynamic.py#L126
    form = assemble_form_class(form_entry=form_entry)
    request = mocker.MagicMock(spec=requests.Response)

    # A valid CollectDataPlugin requires a DynamicForm, a FormEntry, and a post request
    plugin = CollectDataPlugin()
    plugin.run(form=form,
               form_entry=form_entry,
               request=request)

    surveys = Survey.objects.all()

    assert len(surveys) == 1
