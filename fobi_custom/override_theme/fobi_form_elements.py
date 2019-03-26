from fobi.base import form_element_plugin_widget_registry
from fobi.contrib.themes.bootstrap3 import UID

from fobi_custom.plugins.pldp.form_elements.fields.age_single.widgets \
     import BasePLDPAgeSinglePluginWidget
from fobi_custom.plugins.pldp.form_elements.fields.age_multiple.widgets \
     import BasePLDPAgeMultiplePluginWidget

from fobi_custom.plugins.pldp.form_elements.fields.gender_single.widgets \
     import BasePLDPGenderSinglePluginWidget
from fobi_custom.plugins.pldp.form_elements.fields.gender_multiple.widgets \
          import BasePLDPGenderMultiplePluginWidget


class PLDPAgeSinglePluginWidget(BasePLDPAgeSinglePluginWidget):
    """PLDPAgeSinglePluginWidget."""

    theme_uid = UID  # Theme for which the widget is loaded


class PLDPAgeMultiplePluginWidget(BasePLDPAgeMultiplePluginWidget):
    """PLDPAgeMultiplePluginWidget."""

    theme_uid = UID  # Theme for which the widget is loaded


class PLDPGenderSinglePluginWidget(BasePLDPGenderSinglePluginWidget):
    """PLDPGenderSinglePluginWidget."""

    theme_uid = UID  # Theme for which the widget is loaded


class PLDPGenderMultiplePluginWidget(BasePLDPGenderMultiplePluginWidget):
    """PLDPGenderMultiplePluginWidget."""

    theme_uid = UID  # Theme for which the widget is loaded


form_element_plugin_widget_registry.register(PLDPAgeSinglePluginWidget)
form_element_plugin_widget_registry.register(PLDPAgeMultiplePluginWidget)
form_element_plugin_widget_registry.register(PLDPGenderSinglePluginWidget)
form_element_plugin_widget_registry.register(PLDPGenderMultiplePluginWidget)
