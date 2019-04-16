import json
from datetime import datetime
from django.utils.timezone import get_current_timezone
from django.utils.translation import ugettext_lazy as _

from fobi.base import FormHandlerPlugin, form_handler_plugin_registry
from fobi.models import FormElementEntry

from pldp.models import Study, Location, Survey, SurveyRow, SurveyComponent


class CollectDataPlugin(FormHandlerPlugin):
    """Just Spaces data handler plugin."""

    uid = "collect_data"
    name = _("Collect data")

    def run(self, form_entry, request, form, form_element_entries=None):
        """To be executed by handler."""

        self.timezone = get_current_timezone()
        self.today = datetime.now(tz=self.timezone).date()

        meta_elements = ['total', 'time_start', 'time_stop', 'survey_method', 'survey_representation']
        self.form = form
        self.form_id = form_entry.id

        location = Location.objects.get(id=form_entry.surveyformentry.location.id)
        study = Study.objects.get(id=form_entry.surveyformentry.study.id)

        total = get_saved_data(self, 'total', 1)
        datetime_start = get_saved_data(self, 'time_start')

        # if the survey form has a value for time_stop, use that. otherwise,
        # use submission time
        datetime_stop = get_saved_data(self, 'time_stop', datetime.now(tz=self.timezone))
        method = get_saved_data(self, 'survey_method')
        representation = get_saved_data(self, 'survey_representation')

        new_survey = Survey.objects.create(
            study=study,
            form_id=self.form_id,
            location=location,
            time_start=datetime_start,
            time_stop=datetime_stop,
            method=method,
            representation=representation,
        )

        new_survey_row = SurveyRow.objects.create(
            survey=new_survey,
            total=total
        )

        form_elements = FormElementEntry.objects.filter(form_entry_id=self.form_id).exclude(plugin_uid__in=meta_elements)

        for form_element in form_elements:

            element_info = get_element_info(self, form_element)

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


def get_element_info(self, form_element):
    plugin_data = form_element.plugin_data
    json_plugin_data = json.loads(plugin_data)

    if 'text' in json_plugin_data.keys():
        return None

    else:
        name = json_plugin_data['name']

        element_info = {
            'name': name,
            'saved_data': self.form.cleaned_data[name],
            'label': json_plugin_data['label'],
            'type': form_element.plugin_uid,
            'position': form_element.position,
        }

        return element_info


def get_element_data(self, form_element):
    element_info = get_element_info(self, form_element)
    saved_data = element_info['saved_data']

    return saved_data


def get_saved_data(self, plugin_uid, default_value=''):
    try:
        form_element = FormElementEntry.objects.get(form_entry_id=self.form_id, plugin_uid=plugin_uid)
        saved_data = get_element_data(self, form_element)
        if (plugin_uid in ['time_start', 'time_stop']) and saved_data:
            saved_data = datetime.combine(self.today, saved_data).replace(tzinfo=self.timezone)
    except FormElementEntry.DoesNotExist:
        saved_data = default_value

    return saved_data


form_handler_plugin_registry.register(CollectDataPlugin)
