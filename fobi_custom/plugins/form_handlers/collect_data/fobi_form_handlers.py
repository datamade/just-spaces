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

        self.form = form
        self.form_id = form_entry.id

        new_survey_info = {}

        new_survey_info['location'] = Location.objects.get(id=form_entry.surveyformentry.location.id)
        new_survey_info['study'] = Study.objects.get(id=form_entry.surveyformentry.study.id)

        meta_elements = [('time_start', ''),
                         ('time_stop', datetime.now(tz=self.timezone)),
                         ('time_character', ''),
                         ('representation', ''),
                         ('microclimate', ''),
                         ('temperature_c', None),
                         ('method', 'Digital application')]

        new_survey_info['form_id'] = self.form_id

        for (plugin_uid, default) in meta_elements:
            new_survey_info[plugin_uid] = get_saved_data(self, plugin_uid, default)

        new_survey = Survey.objects.create(**new_survey_info)

        total = get_saved_data(self, 'total', 1)

        new_survey_row = SurveyRow.objects.create(
            survey=new_survey,
            total=total
        )

        meta_element_names = [name for (name, default) in meta_elements]

        form_elements = FormElementEntry.objects.filter(form_entry_id=self.form_id).exclude(plugin_uid__in=meta_element_names)

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
