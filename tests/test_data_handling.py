import pytest
import requests
import json
import datetime

from fobi_custom.plugins.form_handlers.collect_data.fobi_form_handlers import CollectDataPlugin
from fobi.dynamic import assemble_form_class

from pldp.models import Survey, SurveyRow, SurveyComponent


@pytest.mark.django_db
def test_data_handler(survey_form_entry, location, study, form_element_float,
                      form_element_help_text, form_element_time_start, mocker):
    """Tests the custom Fobi data handler by instantiating a sample
    survey, surveyrow, and surveycomponent with saved data"""

    float_data = json.loads(form_element_float.plugin_data)
    submitted_float_data = 5

    time_start_data = json.loads(form_element_time_start.plugin_data)
    submitted_time_start_data = datetime.time(5, 45, 00)

    request = mocker.MagicMock(spec=requests.Response)
    form_class = assemble_form_class(form_entry=survey_form_entry)

    form_class = assemble_form_class(form_entry=survey_form_entry)
    form = form_class(data={float_data['name']: submitted_float_data,
                            time_start_data['name']: submitted_time_start_data})

    assert form.is_valid()

    plugin = CollectDataPlugin()
    plugin.run(form=form,
               form_entry=survey_form_entry,
               request=request)

    survey = Survey.objects.first()
    rows = SurveyRow.objects.filter(survey=survey)

    row = rows[0]
    components = SurveyComponent.objects.filter(row=row)
    component = components[0]

    assert len(rows) == 1
    assert len(components) == 1

    assert survey.id
    assert survey.time_start
    assert survey.location == location
    assert survey.study == study

    assert row.id
    assert row.total
    assert row.survey == survey

    assert component.id
    assert component.detail_level == 'basic'
    assert component.name == float_data['name']
    assert component.label == float_data['label']
    assert component.type == form_element_float.plugin_uid
    assert component.position == form_element_float.position
    assert float(component.saved_data) == submitted_float_data
    assert component.row == row
