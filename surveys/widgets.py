import json

from django.forms.widgets import SelectMultiple

from surveys import models


class MultiSelectGeometryWidget(SelectMultiple):
    '''
    Widget for displaying and selecting multiple geometries.
    '''
    input_type = 'select'
    template_name = 'partials/multiselect-geometry-widget.html'

    def __init__(self, attrs=None):
        '''
        Make the select form input hidden so that the user only interacts
        with the map widget.
        '''
        if attrs is None:
            updated_attrs = {'style': 'display:none'}
        else:
            updated_attrs = attrs.copy()
            updated_attrs['style'] = 'display:none'

        super().__init__(updated_attrs)

    def get_context(self, name, value, attrs):
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
        return context
