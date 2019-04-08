import pytest
import requests
import json
from django.urls import reverse

from fobi_custom.plugins.form_handlers.collect_data.fobi_form_handlers import CollectDataPlugin
from fobi.dynamic import assemble_form_class

from pldp.models import Survey, SurveyRow, SurveyComponent


@pytest.mark.django_db
def test_data_handler(form_entry, location, study, form_element, mocker):
    """Tests the custom Fobi data handler by instantiating a sample
    survey, surveyrow, and surveycomponent with saved data"""

    component_data = json.loads(form_element.plugin_data)
    saved_data = 5

    request = mocker.MagicMock(spec=requests.Response)
    form_class = assemble_form_class(form_entry=form_entry)

    form_class = assemble_form_class(form_entry=form_entry)
    form = form_class(data={component_data['name']: saved_data})

    assert form.is_valid()

    plugin = CollectDataPlugin()
    plugin.run(form=form,
               form_entry=form_entry,
               request=request)

    survey = Survey.objects.first()
    rows = SurveyRow.objects.filter(survey=survey)

    row = rows[0]
    components = SurveyComponent.objects.filter(row=row)
    component = components[0]

    assert len(rows) == 1
    assert len(components) == 1

    assert survey.id
    assert survey.time_stop
    assert survey.location == location
    assert survey.study == study

    assert row.id
    assert row.total
    assert row.survey == survey

    assert component.id
    assert component.detail_level == 'basic'
    assert component.name == component_data['name']
    assert component.label == component_data['label']
    assert component.type == form_element.plugin_uid
    assert component.position == form_element.position
    assert float(component.saved_data) == saved_data
    assert component.row == row


@pytest.mark.django_db
def test_survey_submitted_list(user, survey, client, form_entry):
    client.force_login(user)
    url = reverse('surveys-submitted-list')
    response = client.get(url)

    surveys_submitted = response.context['surveys_submitted']

    assert response.status_code == 200
    assert len(surveys_submitted) == 1
    assert str(surveys_submitted.first().form_title) == 'Sample Form Entry'
