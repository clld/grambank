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


def includeme(config):
    pass
