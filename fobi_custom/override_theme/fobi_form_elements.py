from fobi.base import form_element_plugin_widget_registry
from fobi.contrib.themes.bootstrap3 import UID

from fobi_custom.plugins.form_elements.fields.age.widgets \
     import BasePLDPAgePluginWidget

from fobi_custom.plugins.form_elements.fields.gender.widgets \
          import BasePLDPGenderPluginWidget

from fobi_custom.plugins.form_elements.fields.study.widgets \
          import BasePLDPStudyPluginWidget
#
# from fobi_custom.plugins.form_elements.fields.time_start.widgets \
#           import BasePLDPTimeStartPluginWidget
#
# from fobi_custom.plugins.form_elements.fields.time_stop.widgets \
#           import BasePLDPTimeStopPluginWidget

from fobi_custom.plugins.form_elements.fields.survey_representation.widgets \
          import BasePLDPSurveyRepresentationPluginWidget

from fobi_custom.plugins.form_elements.fields.survey_method.widgets \
          import BasePLDPSurveyMethodPluginWidget



class PLDPAgePluginWidget(BasePLDPAgePluginWidget):
    """PLDPAgePluginWidget."""

    theme_uid = UID  # Theme for which the widget is loaded


class PLDPGenderPluginWidget(BasePLDPGenderPluginWidget):
    """PLDPGenderPluginWidget."""

    theme_uid = UID  # Theme for which the widget is loaded


class PLDPStudyPluginWidget(BasePLDPStudyPluginWidget):
    """PLDPStudyPluginWidget."""

    theme_uid = UID  # Theme for which the widget is loaded

# class PLDPTimeStartPluginWidget(BasePLDPTimeStartPluginWidget):
#     """PLDPTimeStartPluginWidget."""
#
#     theme_uid = UID  # Theme for which the widget is loaded
#
# class PLDPTimeStopPluginWidget(BasePLDPTimeStopPluginWidget):
#     """PLDPTimeStopPluginWidget."""
#
#     theme_uid = UID  # Theme for which the widget is loaded


class PLDPSurveyRepresentationPluginWidget(BasePLDPSurveyRepresentationPluginWidget):
    """PLDPSurveyRepresentationPluginWidget."""

    theme_uid = UID  # Theme for which the widget is loaded


class PLDPSurveyMethodPluginWidget(BasePLDPSurveyMethodPluginWidget):
    """PLDPSurveyMethodPluginWidget."""

    theme_uid = UID  # Theme for which the widget is loaded


form_element_plugin_widget_registry.register(PLDPAgePluginWidget)
form_element_plugin_widget_registry.register(PLDPGenderPluginWidget)
form_element_plugin_widget_registry.register(PLDPStudyPluginWidget)
# form_element_plugin_widget_registry.register(PLDPTimeStartPluginWidget)
# form_element_plugin_widget_registry.register(PLDPTimeStopPluginWidget)
form_element_plugin_widget_registry.register(PLDPSurveyRepresentationPluginWidget)
form_element_plugin_widget_registry.register(PLDPSurveyMethodPluginWidget)
