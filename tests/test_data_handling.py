import pytest
import requests
import json

from fobi_custom.plugins.form_handlers.collect_data.fobi_form_handlers import CollectDataPlugin
from fobi.dynamic import assemble_form_class

from pldp.models import Survey, SurveyRow, SurveyComponent


@pytest.mark.django_db
def test_data_handler(form_entry, location, study, form_element, mocker):
    component_data = json.loads(form_element.plugin_data)

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
    rows = SurveyRow.objects.filter(survey=survey)

    # Grab the row object itself out of the filtered row queryset, in order to
    # find its linked components
    row = rows[0]
    components = SurveyComponent.objects.filter(row=row)
    component = components[0]

    # Check that the handler has created a single row and linked component
    assert len(rows) == 1
    assert len(components) == 1

    # Check survey has the correct values
    assert survey.id
    assert survey.time_stop
    assert survey.location == location
    assert survey.study == study

    # Check row has the correct values
    assert row.id
    assert row.total
    assert row.survey == survey

    # Check component has the correct values
    assert component.id
    assert component.detail_level == 'basic'
    assert component.name == component_data['name']
    assert component.label == component_data['label']
    assert component.type == form_element.plugin_uid
    assert component.position == form_element.position
    assert component.row == row
