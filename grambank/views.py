from grambank.maps import IsoGlossMap


def about(req):
    return {'data': 'goes here', 'map': IsoGlossMap(None, req)}


def coverage(req):
    return {}
