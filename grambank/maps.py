from clld.web.maps import Map, Layer

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
    
class DeepFamilyMap(Map):
    def __init__(self, ctx, req, eid='map', icon_map=None):
        super(DeepFamilyMap, self).__init__(ctx, req, eid=eid)
        self.icon_map = icon_map or {} #TODO make this point to a URL with a .png
        self.deepfamid = ctx.id
        self.deepfamname = ctx.id
        self.protolanguages = ([(ctx.family1_pk, ctx.family1.name, ctx.family1_longitude, ctx.family1_latitude, ctx.family1.name)] if ctx.family1_latitude else []) + ([(ctx.family2_pk, ctx.family2.name, ctx.family2_longitude, ctx.family2_latitude, ctx.family2.name)] if ctx.family2_latitude else [])
              
    def get_layers(self):
        properties = {"layer": "deepfamily"} #self.deepfamid, "name": self.deepfamname}
        features = [{"type": "Feature", "geometry": {'type': 'Point', 'coordinates': (lon, lat)}, "properties": {'name': name, 'icon': self.icon_map[pk], "id": id_}, "pk": pk, "description": None, "longitude": lon, "latitude": lat, "markup_description": None, "jsondata": {}} for (pk, name, lon, lat, id_) in self.protolanguages]
        #yield Layer(self.id, self.name, {"type": "FeatureCollection", "properties": properties, "features": features})
        #print self.id
        #print features
        yield Layer("deepfamily", self.deepfamname,
            {
                "type": "FeatureCollection",
                "properties": properties,
                "features": features
            })
    
    def get_options(self):
        res = {'max_zoom': 12}
        res['sidebar'] = True
        res['zoom'] = 6
        res['no_link'] = True
        res['no_popup'] = True
        return res


#<script>$(window).load(function() {CLLD.map("map", {"taga1270": {"type": "FeatureCollection", "properties": {"layer": ""}, "features": [{"geometry": {"type": "Point", "coordinates": [121.747, 14.06]}, "type": "Feature", "properties": {"name": "Tagalog", "language": {"markup_description": null, "name": "Tagalog", "description": null, "jsondata": {}, "longitude": 121.747, "latitude": 14.06, "pk": 403, "id": "taga1270", "macroarea": "Papunesia", "family_pk": 4}, "icon": "http://localhost:6543/clld-static/icons/cdd0000.png"}, "id": "taga1270"}]}}, {"sidebar": true, "no_link": true, "center": [14.06, 121.747], "no_popup": true, "zoom": 3});});</script>
#<script>$(window).load(function() {CLLD.map("map", {"taga1270": {"type": "FeatureCollection", "properties": {"layer": ""}, "features": [{"geometry": {"type": "Point", "coordinates": [133.618, -1.18016]}, "type": "Feature", "properties": {"icon": "http://localhost:6543/clld-static/icons/c00ff00.png"}}, {"geometry": {"type": "Point", "coordinates": [134.037, -1.18016]}, "type": "Feature", "properties": {"icon": "http://localhost:6543/clld-static/icons/cff0000.png"}}]}}, {"sidebar": true, "max_zoom": 12, "zoom": 6});});</script>
#<script>$(window).load(function() {CLLD.map("map", {"isogloss": {"type": "FeatureCollection", "properties": {"layer": "proto-East Bird's Head x proto-Hatam-Mansim ", "name": "proto-East Bird's Head x proto-Hatam-Mansim "}, "features": [{"geometry": {"type": "Point", "coordinates": [133.618, -1.18016]}, "type": "Feature", "properties": {"icon": "http://localhost:6543/clld-static/icons/c00ff00.png"}}, {"geometry": {"type": "Point", "coordinates": [134.037, -1.18016]}, "type": "Feature", "properties": {"icon": "http://localhost:6543/clld-static/icons/cff0000.png"}}]}}, {"sidebar": true, "max_zoom": 12, "zoom": 6});});</script>
#$(window).load(function() {CLLD.map("map", {"taga1270": {"type": "FeatureCollection", "properties": {"layer": "proto-East Bird's Head x proto-Hatam-Mansim ", "name": "proto-East Bird's Head x proto-Hatam-Mansim "}, "features": [{"geometry": {"type": "Point", "coordinates": [133.618, -1.18016]}, "type": "Feature", "properties": {"icon": "http://localhost:6543/clld-static/icons/c00ff00.png"}}, {"geometry": {"type": "Point", "coordinates": [134.037, -1.18016]}, "type": "Feature", "properties": {"icon": "http://localhost:6543/clld-static/icons/cff0000.png"}}]}}, {"sidebar": true, "max_zoom": 12, "zoom": 6});});
def includeme(config):
    config.register_map('deepfamily', DeepFamilyMap)

