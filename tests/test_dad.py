# Tests for the Data Analysis Designer (DAD)
import pytest
import uuid

from django.urls import reverse
from pldp.models import SurveyComponent

from surveys import models
from fobi_custom.plugins.form_elements.fields import types as fobi_types


@pytest.fixture
def survey_submitted_setup(survey, survey_row, survey_component):
    # Set up necessary fixtures for the surveys-submitted-detail view
    pass


def create_formset_data(initial, total, forms):
    # Helper function to create POST data for a formset in the DAD.
    # Arguments:
    #   * initial (int): Initial number of forms on the page at load time
    #   * total (int): Total number of forms on the page at POST time
    #   * forms (iterable): Iterable of dictionaries, each one representing the
    #                       field value for a form in the formset
    output_form = {
        # Initialize with management form data
        'form-INITIAL_FORMS': initial,
        'form-TOTAL_FORMS': total,
    }

    for idx, form in enumerate(forms):
        prefix = 'form-' + str(idx) + '-'
        for field_name, value in form.items():
            output_form[prefix + field_name] = value

    return output_form


def test_create_chart(client, survey_form_entry, survey_submitted_setup):
    # Test that the DAD can create a chart
    chart_data = [{'short_description': '__foobar__', 'order': 1}]
    post_data = create_formset_data(0, len(chart_data), chart_data)

    create_url = reverse('surveys-submitted-detail',
                         kwargs={'form_entry_id': survey_form_entry.id})

    create_response = client.post(create_url, data=post_data)

    assert create_response.status_code == 200
    assert 'alert-success' in create_response.content.decode('utf-8')
    assert chart_data[0]['short_description'] in create_response.content.decode('utf-8')

    new_chart = models.SurveyChart.objects.get(id=1)
    assert new_chart.short_description == chart_data[0]['short_description']


def test_basic_chart_display(client, survey_form_entry, survey_submitted_setup):
    # Test that the DAD displays charts in the correct number and order
    chart_data = [
        {'short_description': '__bar__', 'order': 2},
        {'short_description': '__foo__', 'order': 1},
        {'short_description': '__baz__', 'order': 3}
    ]
    post_data = create_formset_data(0, len(chart_data), chart_data)

    create_url = reverse('surveys-submitted-detail',
                         kwargs={'form_entry_id': survey_form_entry.id})

    create_response = client.post(create_url, data=post_data)

    assert create_response.status_code == 200
    assert 'alert-success' in create_response.content.decode('utf-8')

    # Make sure the charts are displayed in the correct order
    sorted_charts = sorted(chart_data, key=lambda chart: chart['order'])
    for idx, form in enumerate(sorted_charts):
        assert form['short_description'] in create_response.content.decode('utf-8')
        if idx == len(sorted_charts)-1:
            prev_desc = sorted_charts[idx-1]['short_description']
            assert prev_desc in create_response.content.decode('utf-8').split(form['short_description'])[0]
        else:
            next_desc = sorted_charts[idx+1]['short_description']
            assert next_desc in create_response.content.decode('utf-8').split(form['short_description'])[1]


def test_delete_chart(client, survey_form_entry, survey_submitted_setup):
    # Test that the DAD can delete a chart
    chart_data = {
        'short_description': '__delete_me__',
        'order': 1,
        'form_entry': survey_form_entry
    }
    new_chart = models.SurveyChart.objects.create(**chart_data)

    url = reverse('surveys-submitted-detail',
                  kwargs={'form_entry_id': survey_form_entry.id})
    get_response = client.get(url)

    assert get_response.status_code == 200
    assert chart_data['short_description'] in get_response.content.decode('utf-8')

    forms_to_delete = [chart_data.copy()]
    forms_to_delete[0].update({'id': new_chart.id, 'DELETE': True})
    post_data = create_formset_data(1, len(forms_to_delete), forms_to_delete)

    delete_response = client.post(url, data=post_data)

    assert delete_response.status_code == 200
    assert 'alert-success' in delete_response.content.decode('utf-8')
    assert chart_data['short_description'] not in delete_response.content.decode('utf-8')


def test_ignore_new_removed_chart(client, survey_form_entry, survey_submitted_setup):
    # Test that the DAD will not create a new chart if the 'delete' field is checked
    chart_data = [{'short_description': '__delete_me__', 'order': 1, 'DELETE': True}]
    post_data = create_formset_data(0, len(chart_data), chart_data)

    create_url = reverse('surveys-submitted-detail',
                         kwargs={'form_entry_id': survey_form_entry.id})

    create_response = client.post(create_url, data=post_data)

    assert create_response.status_code == 200
    assert 'alert-success' in create_response.content.decode('utf-8')
    assert chart_data[0]['short_description'] not in create_response.content.decode('utf-8')


def test_valid_type_display(client, survey, survey_form_entry, survey_row):
    # Test that all question types in the DAD_VALID_TYPES list get displayed as
    # primary source options in the DAD, and that other types don't get displayed.
    counter = 1
    valid_components = []
    for idx, component_type in enumerate(fobi_types.DAD_VALID_TYPES):
        valid_component = SurveyComponent.objects.create(
            detail_level='basic',
            name=str(uuid.uuid4()),
            label='Test label %d' % counter,
            type=component_type,
            position=idx+1,
            saved_data='foo',
            row=survey_row,
        )
        valid_components.append(valid_component)
        counter += 1

    invalid_components = []
    for idx, component_type in enumerate(fobi_types.DAD_INVALID_TYPES):
        invalid_component = SurveyComponent.objects.create(
            detail_level='basic',
            name=str(uuid.uuid4()),
            label='Test label %d' % counter,
            type=component_type,
            position=idx+1,
            saved_data='foo',
            row=survey_row,
        )
        invalid_components.append(invalid_component)
        counter += 1

    get_url = reverse('surveys-submitted-detail',
                      kwargs={'form_entry_id': survey_form_entry.id})
    get_response = client.get(get_url)
    assert get_response.status_code == 200

    for valid_component in valid_components:
        assert valid_component.name in get_response.content.decode('utf-8')
    for invalid_component in invalid_components:
        assert invalid_component.name not in get_response.content.decode('utf-8')
