import json
from fobi.base import FormHandlerPlugin, form_handler_plugin_registry
from django.utils.translation import ugettext_lazy as _
from .forms import CollectDataForm

from pldp.models import Study, Location, Survey, SurveyRow #, SurveyComponent

class CollectDataPlugin(FormHandlerPlugin):
    """Just Spaces data handler plugin."""

    uid = "collect_data"
    name = _("Collect data")

    def run(self, form_entry, request, form):
        """To be executed by handler."""

        location = Location.objects.first()
        study = Study.objects.first()
        total = 5

        new_survey = Survey(study=study,
                            location=location)
        new_survey.save()

        new_survey_row = SurveyRow(
            survey=new_survey,
            total=total
        )
        new_survey_row.save()

        # for survey_component in all_cleaned_data:
        #     new_survey_component = SurveyComponent()
        #     new_survey_component.save()

def plugin_data_repr(self):
    """Human readable representation of plugin data.

    :return string:
    """
    return self.data.__dict__

form_handler_plugin_registry.register(CollectDataPlugin)
