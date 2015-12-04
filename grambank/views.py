from grambank.maps import IsoGlossMap
#from stats_util import parsimony_stability

from clld import RESOURCES
from clld.db.meta import DBSession
from models import GrambankLanguage, Feature


def about(req):
    return {'data': req, 'map': IsoGlossMap(None, req)}

def introduction(req):
    data = [k for k in DBSession.query(GrambankLanguage.id, Feature.id)]
    #data = [rsc for rsc in RESOURCES if rsc.name in ['language']]
    return {'data': [len(data)] + data, 'map': IsoGlossMap(None, req)}
    #lv = req_to_lfs()
    #clf = req_to_clf()
    #return parsimony_stability(lf, clf) #{'data': 'goes here', 'map': IsoGlossMap(None, req)}


