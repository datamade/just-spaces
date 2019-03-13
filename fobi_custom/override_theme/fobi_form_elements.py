from fobi.base import form_element_plugin_widget_registry
from fobi.contrib.themes.bootstrap3 import UID

from fobi_custom.plugins.pldp.form_elements.fields.age.widgets \
     import BasePLDPAgePluginWidget

from fobi_custom.plugins.pldp.form_elements.fields.gender.widgets \
          import BasePLDPGenderPluginWidget

from fobi_custom.plugins.pldp.form_elements.fields.study.widgets \
          import BasePLDPStudyPluginWidget


class PLDPAgePluginWidget(BasePLDPAgePluginWidget):
    """PLDPAgePluginWidget."""

    theme_uid = UID  # Theme for which the widget is loaded


class PLDPGenderPluginWidget(BasePLDPGenderPluginWidget):
    """PLDPGenderPluginWidget."""

    theme_uid = UID  # Theme for which the widget is loaded


class PLDPStudyPluginWidget(BasePLDPStudyPluginWidget):
    """PLDPStudyPluginWidget."""

    theme_uid = UID  # Theme for which the widget is loaded


form_element_plugin_widget_registry.register(PLDPAgePluginWidget)
form_element_plugin_widget_registry.register(PLDPGenderPluginWidget)
form_element_plugin_widget_registry.register(PLDPStudyPluginWidget)
