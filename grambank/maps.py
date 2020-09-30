from clld.web.maps import ParameterMap, Layer
from clld.web.util import helpers


class FeatureMap(ParameterMap):
    def __init__(self, *args, **kw):
        self.family = kw.pop('family', None)
        ParameterMap.__init__(self, *args, **kw)

    def get_layers(self):
        for de in self.ctx.domain:
            yield Layer(
                de.id,
                de.name,
                self.req.resource_url(
                    self.ctx, ext='geojson',
                    _query=dict(
                        domainelement=str(de.id),
                        family=self.family.id if self.family else None,
                        **self.req.query_params)
                ),
                marker=helpers.map_marker_img(self.req, de, marker=self.map_marker))

    #def get_default_options(self):
    #    return {'hash': True, 'icon_size': 15, 'base_layer': "Esri.WorldPhysical"}


def includeme(config):
    config.register_map('parameter', FeatureMap)
