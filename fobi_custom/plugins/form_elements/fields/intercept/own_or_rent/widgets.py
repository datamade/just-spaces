from fobi.base import FormElementPluginWidget


class BaseOwnOrRentPluginWidget(FormElementPluginWidget):
    """BaseOwnOrRentPluginWidget."""

    # Same as ``uid`` value of the ``OwnOrRentPlugin``.
    plugin_uid = "own_or_rent"
