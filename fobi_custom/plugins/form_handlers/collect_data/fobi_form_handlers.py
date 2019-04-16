import json
import datetime
from django.utils.timezone import get_current_timezone
from django.utils.translation import ugettext_lazy as _

from fobi.base import FormHandlerPlugin, form_handler_plugin_registry
from fobi.models import FormEntry, FormElementEntry

from pldp.models import Study, Location, Survey, SurveyRow, SurveyComponent


class CollectDataPlugin(FormHandlerPlugin):
    """Just Spaces data handler plugin."""

    uid = "collect_data"
    name = _("Collect data")

    def run(self, form_entry, request, form, form_element_entries=None):
        """To be executed by handler."""

        form_id = form_entry.id

        location = Location.objects.get(id=form_entry.surveyformentry.location.id)
        study = Study.objects.get(id=form_entry.surveyformentry.study.id)

        try:
            total_element = FormElementEntry.objects.get(form_entry_id=form_id, plugin_uid='total')
            total_element_info = get_element_info(self, total_element, form)
            total = total_element_info['saved_data']
        except FormElementEntry.DoesNotExist:
            total = 1

        # Here we are using PLDP's survey end time value to record time
        # of submission
        time_stop = datetime.datetime.now(tz=get_current_timezone())

        new_survey = Survey.objects.create(
            study=study,
            form_id=form_id,
            location=location,
            time_stop=time_stop
        )

        new_survey_row = SurveyRow.objects.create(
            survey=new_survey,
            total=total
        )

        form_elements = FormElementEntry.objects.filter(form_entry_id=form_id).exclude(plugin_uid='total')

        for form_element in form_elements:

            element_info = get_element_info(self, form_element, form)

            if element_info:
                SurveyComponent.objects.create(
                    row=new_survey_row,
                    name=element_info['name'],
                    label=element_info['label'],
                    type=element_info['type'],
                    position=element_info['position'],
                    saved_data=element_info['saved_data']
                )


def plugin_data_repr(self):
    """Human readable representation of plugin data.

    :return string:
    """
    return self.data.__dict__


def get_element_info(self, form_element, form):
    plugin_data = form_element.plugin_data
    json_plugin_data = json.loads(plugin_data)

    if 'text' in json_plugin_data.keys():
        return None

    else:
        name = json_plugin_data['name']

        element_info = {
            'name': name,
            'saved_data': form.cleaned_data[name],
            'label': json_plugin_data['label'],
            'type': form_element.plugin_uid,
            'position': form_element.position,
        }

        return element_info


form_handler_plugin_registry.register(CollectDataPlugin)
