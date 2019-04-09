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

        # These are placeholders. Location and Study are required fields on all
        # surveys, and we need to decide if they'll be form elements or
        # part of the form entry itself. See https://github.com/datamade/just-spaces/issues/63
        # Similarly, total should be a required field in observational surveys, and
        # default to 1 for intercept surveys.
        location = Location.objects.first()
        study = Study.objects.first()

        total = 5

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

        form_entry = FormEntry.objects.get(id=form_id)
        form_elements = FormElementEntry.objects.filter(form_entry=form_entry)

        for element in form_elements:

            plugin_data = element.plugin_data
            json_plugin_data = json.loads(plugin_data)

            # Check if an element is help text. If it is, skip it
            if 'text' in json_plugin_data.keys():
                continue

            else:
                name = json_plugin_data['name']

                label = json_plugin_data['label']
                type = element.plugin_uid
                position = element.position

                saved_data = form.cleaned_data[name]

                SurveyComponent.objects.create(
                    row=new_survey_row,
                    name=name,
                    label=label,
                    type=type,
                    position=position,
                    saved_data=saved_data
                )


def plugin_data_repr(self):
    """Human readable representation of plugin data.

    :return string:
    """
    return self.data.__dict__


form_handler_plugin_registry.register(CollectDataPlugin)
