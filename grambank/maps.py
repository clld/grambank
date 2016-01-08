from clld.web.maps import Map, Layer
from clld.web.adapters.geojson import GeoJson

class IsoGlossMap(Map):
    def get_layers(self):
        yield Layer(
            'isogloss',
            'iso gloss',
            {
                "type": "FeatureCollection",
                "properties": {"layer": "isogloss", "name": "iso gloss"},
                "features": [
                    {
                        "type": "Feature",
                        "geometry": {
                            "type": "LineString",
                            "coordinates": [
                                [-100, 40],
                                [-105, 45],
                                [-110, 45],
                                [-110, 55]]
                        },
                        "properties": {
                            "name": "Dinagat Islands"
                        }
                    }
                ]
            })



class LanguoidGeoJson(GeoJson):
    def __init__(self, obj, icon_map=None):
        super(LanguoidGeoJson, self).__init__(obj)
        self.icon_map = icon_map or {}

    def feature_iterator(self, ctx, req):
        res = [(ctx.pk, ctx.name, ctx.longitude, ctx.latitude, ctx.id)] \
            if ctx.latitude else []
        return res + list(ctx.get_geocoords())

    def featurecollection_properties(self, ctx, req):
        return {'layer': getattr(ctx, 'id', '')}

    def feature_properties(self, ctx, req, feature):
        if self.icon_map:
            return {'icon': self.icon_map[feature[0]], 'branch': feature[0]}
        return {}        
        
class DeepFamilyMap(Map):
    def __init__(self, ctx, req, eid='map', icon_map=None):
        super(DeepFamilyMap, self).__init__(ctx, req, eid=eid)
        self.icon_map = icon_map or {}
        
        
    def get_layers(self):
        yield Layer(
            self.ctx.id,
            self.ctx.id,
            LanguoidGeoJson(
                self.ctx, self.icon_map).render(self.ctx, self.req, dump=False))

    def get_options(self):
        res = {'max_zoom': 12}
        res['sidebar'] = True
        res['zoom'] = 6
        return res
      
def includeme(config):
    pass
    #config.register_map('deepfamily', DeepFamilyMap)

