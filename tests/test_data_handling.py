import pytest
import requests

from fobi_custom.plugins.form_handlers.collect_data.fobi_form_handlers import CollectDataPlugin
from fobi.dynamic import assemble_form_class

from pldp.models import Survey, SurveyRow, SurveyComponent


@pytest.mark.django_db
def test_data_handler(form_entry, location, study, form_element, mocker):
    request = mocker.MagicMock(spec=requests.Response)
    form = assemble_form_class(form_entry=form_entry)

    # form.cleaned_data['c75e27cf-4d8f-49dc-bb15-da8137dac247'] = 5

    # A valid CollectDataPlugin requires a DynamicForm, a FormEntry, and a post request
    plugin = CollectDataPlugin()
    plugin.run(form=form,
               form_entry=form_entry,
               request=request)

    # Check that a survey has been created with a linked row and component
    survey = Survey.objects.first()
    row = SurveyRow.objects.filter(survey=survey)
    component = SurveyComponent.objects.filter(row=row[0])

    assert (len(row), len(component)) == (1, 1)
