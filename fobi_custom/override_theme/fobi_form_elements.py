from fobi.base import form_element_plugin_widget_registry
from fobi.contrib.themes.bootstrap3 import UID

from fobi_custom.plugins.form_elements.fields.age.widgets \
     import BasePLDPAgePluginWidget

from fobi_custom.plugins.form_elements.fields.gender.widgets \
          import BasePLDPGenderPluginWidget

from fobi_custom.plugins.form_elements.fields.study.widgets \
          import BasePLDPStudyPluginWidget

from fobi_custom.plugins.form_elements.fields.time_start.widgets \
          import BaseTimeStartPluginWidget

from fobi_custom.plugins.form_elements.fields.time_stop.widgets \
          import BaseTimeStopPluginWidget

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


class TimeStartPluginWidget(BaseTimeStartPluginWidget):
    """TimeStartPluginWidget."""

    theme_uid = UID  # Theme for which the widget is loaded


class TimeStopPluginWidget(BaseTimeStopPluginWidget):
    """TimeStopPluginWidget."""

    theme_uid = UID  # Theme for which the widget is loaded


class PLDPSurveyRepresentationPluginWidget(BasePLDPSurveyRepresentationPluginWidget):
    """PLDPSurveyRepresentationPluginWidget."""

    theme_uid = UID  # Theme for which the widget is loaded


class PLDPSurveyMethodPluginWidget(BasePLDPSurveyMethodPluginWidget):
    """PLDPSurveyMethodPluginWidget."""

    theme_uid = UID  # Theme for which the widget is loaded


form_element_plugin_widget_registry.register(PLDPAgePluginWidget)
form_element_plugin_widget_registry.register(PLDPGenderPluginWidget)
form_element_plugin_widget_registry.register(PLDPStudyPluginWidget)
form_element_plugin_widget_registry.register(TimeStartPluginWidget)
form_element_plugin_widget_registry.register(TimeStopPluginWidget)
form_element_plugin_widget_registry.register(PLDPSurveyRepresentationPluginWidget)
form_element_plugin_widget_registry.register(PLDPSurveyMethodPluginWidget)
