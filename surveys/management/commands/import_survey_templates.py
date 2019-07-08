import os
import json

from django.core.management.base import BaseCommand

from users.models import JustSpacesUser
from surveys.models import SurveyFormEntry
from fobi.models import FormElementEntry

class Command(BaseCommand):
    help = 'Load survey template data into database'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Clearing out old templates...'))
        SurveyFormEntry.objects.filter(is_cloneable='t').delete()

        self.stdout.write(self.style.SUCCESS('Starting new template import...'))

        # templates should be saved in
        # ./survey_template_data/survey_templates.json in the following format:
        #
        # [
        #   {
        #     "name": "Sample Survey Template",
        #     "type": "observational",
        #     "questions": [
        #       {
        #         "plugin_data": "plugin data here with "name" key deleted
        #                         (this will be readded when templated
        #                         questions are loaded into a survey)",
        #         "plugin_uid": "gender_observational",
        #         "position": 1
        #       }
        #     ]
        #   }
        # ]

        filepath = os.path.join('surveys',
                                'survey_template_data',
                                'survey_templates.json'
                                )

        with open(filepath) as json_file:
            survey_templates = json.load(json_file)

            user = JustSpacesUser.objects.first()

            for survey_template in survey_templates:
                new_template = SurveyFormEntry.objects.create(
                    name=survey_template['name'],
                    user=user,
                    is_cloneable='t',
                    type=survey_template['type'],
                )

                for question in survey_template['questions']:
                    new_question = FormElementEntry.objects.create(
                        plugin_data=question['plugin_data'],
                        plugin_uid=question['plugin_uid'],
                        position=question['position'],
                        form_entry=new_template,
                    )

        self.stdout.write(self.style.SUCCESS('Templates created!'))
