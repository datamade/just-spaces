import json

from django.forms.widgets import SelectMultiple


class MultiSelectGeometryWidget(SelectMultiple):
    '''
    Widget for displaying and selecting multiple geometries.
    '''
    input_type = 'select'
    template_name = 'partials/multiselect_geometry_widget.html'

    def __init__(self, attrs=None, choices=(), leaflet_overrides={}):
        """
        Override __init__ to update the config dictionary to make sure that the
        non-map input is always hidden.
        """
        self.leaflet_overrides = leaflet_overrides

        if attrs is None:
            updated_attrs = {'style': 'display:none'}
        else:
            updated_attrs = attrs.copy()
            updated_attrs['style'] = 'display:none'

        super().__init__(attrs=updated_attrs, choices=choices)

    def get_context(self, name, value, attrs):
        """
        Override get_context to create GeoJSON geometries to pass into the template.
        """
        context = super().get_context(name, value, attrs)
        context['json'] = json.dumps({
            'type': 'FeatureCollection',
            'features': [{
                            'type': 'Feature',
                            'geometry': json.loads(choice.geom.json),
                            'properties': {
                                'id': choice.pk,
                            }
                        }
                        for _, choice in self.choices]
        })
        context['settings_overrides'] = self.leaflet_overrides
        return context

    def format_value(self, value):
        """
        Override format_value to make sure that Array values get cast to
        Python lists properly. See: https://stackoverflow.com/a/53216766
        """
        if value is not None and not isinstance(value, (tuple, list)):
            value = value.split(',')
        return super().format_value(value)
