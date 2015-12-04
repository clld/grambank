from collections import defaultdict

from sqlalchemy import select
from pyramid.asset import abspath_from_asset_spec

from clld.util import jsonload
from clld.db.meta import DBSession
from clld.db.models.common import Language
from clld_glottologfamily_plugin.models import Family

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

def coverage(req):
    gl = jsonload(abspath_from_asset_spec('grambank:static/stats_glottolog.json'))

    stats = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
    for ma in gl:
        for dt in gl[ma]:
            ids = gl[ma][dt]

            isolates = select(
                [Language.__table__.c.id]).where(Language.__table__.c.id.in_(ids))
            families = select(
                [Family.__table__.c.id]).where(Family.__table__.c.id.in_(ids))
            stats[ma][dt] = dict(
                glottolog=len(ids),
                grambank=DBSession.query(isolates.union(families).alias('u')).count())
        stats[ma]['total'] = {}
        for src in ['glottolog', 'grambank']:
            stats[ma]['total'][src] = \
                stats[ma]['grammar'][src] + stats[ma]['grammarsketch'][src]
    return dict(stats=stats)
