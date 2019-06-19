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
        Make the actual form input hidden so that the user only interacts
        with the map widget.
        '''
        if attrs is None:
            updated_attrs = {'style': 'display:none'}
        else:
            updated_attrs = attrs.copy()
            updated_attrs['style'] = 'display:none'

        super().__init__(updated_attrs)

    def get_context(self, name, value, attrs):
        if not getattr(self, 'geometry_queryset'):
            raise NameError(
                'MultiSelectGeometryWidgets must be instantiated with a `geometry_queryset` attribute.'
            )

        context = super().get_context(name, value, attrs)

        context['json'] = json.dumps({
            'type': 'FeatureCollection',
            'features': [{
                            'type': 'Feature',
                            'geometry': json.loads(geom.geom.json),
                            'properties': {
                                'id': geom.pk,
                            }
                        }
                        for geom in self.geometry_queryset]
        })

        return context


class CensusTractWidget(MultiSelectGeometryWidget):
    geometry_queryset = models.CensusBlockGroup.objects.all()
