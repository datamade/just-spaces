from fobi.base import form_element_plugin_widget_registry
from fobi.contrib.themes.bootstrap3 import UID

from fobi_custom.plugins.pldp.form_elements.fields.single.age.widgets \
     import BasePLDPAgeSinglePluginWidget
from fobi_custom.plugins.pldp.form_elements.fields.single.gender.widgets \
     import BasePLDPGenderSinglePluginWidget


class PLDPAgeSinglePluginWidget(BasePLDPAgeSinglePluginWidget):
    """PLDPAgeSinglePluginWidget."""

    theme_uid = UID  # Theme for which the widget is loaded


class PLDPGenderSinglePluginWidget(BasePLDPGenderSinglePluginWidget):
    """PLDPGenderSinglePluginWidget."""

    theme_uid = UID  # Theme for which the widget is loaded


form_element_plugin_widget_registry.register(PLDPAgeSinglePluginWidget)
form_element_plugin_widget_registry.register(PLDPGenderSinglePluginWidget)
