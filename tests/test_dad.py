# Tests for the Data Analysis Designer (DAD)
import pytest
from django.urls import reverse

from surveys import models


def create_formset(initial, total, forms):
    # Helper function to create POST data for a formset in the DAD.
    # Arguments:
    #   * initial (int): Number of initial forms on the page
    #   * total (int): Total number of forms on the page
    #   * forms (iterable): Iterable of dictionaries, each one representing the
    #                       field value for a form in the formset
    output_form = {
        # Initialize with management form data
        'form-TOTAL_FORMS': total,
        'form-INITIAL_FORMS': initial,
    }

    for idx, form in enumerate(forms):
        prefix = 'form-' + str(idx) + '-'
        for field_name, value in form.items():
            output_form[prefix + field_name] = value

    return output_form


@pytest.mark.django_db
def test_create_chart(client, survey_form_entry, survey, survey_row, survey_component):
    # Test that the DAD can create a chart
    short_description = 'foobar'
    forms = [{'short_description': short_description, 'order': 1}]
    post_data = create_formset(0, 1, forms)

    create_url = reverse(
        'surveys-submitted-detail',
        kwargs={
            'form_entry_id': survey_form_entry.id
        }
    )

    create_response = client.post(create_url, data=post_data)

    assert create_response.status_code == 200
    assert 'alert-success' in create_response.content.decode('utf-8')
    assert short_description in create_response.content.decode('utf-8')

    new_chart = models.SurveyChart.objects.get(id=1)
    assert new_chart.short_description == short_description


@pytest.mark.django_db
def test_basic_chart_display():
    # Test that the DAD displays charts in the correct number and order (make
    # sure that the chart IDs are in the right order, too)
    pytest.fail()


@pytest.mark.django_db
def test_chart_validation_failure():
    # Test that a DAD chart submitted without a description does not validate
    # and returns appropriate errors
    pytest.fail()


@pytest.mark.django_db
def test_delete_chart():
    # Test that the DAD can delete a chart
    pytest.fail()


@pytest.mark.django_db
def test_ignore_new_removed_chart():
    # Test that the DAD will not create a new chart if the 'delete' field is checked
    pytest.fail()


@pytest.mark.django_db
def test_reorder_charts():
    # Test that the DAD can reorder a chart
    pytest.fail()
