from sqlalchemy.orm import joinedload, joinedload_all

from clld import interfaces
from clld.web.adapters.geojson import GeoJsonParameter
from clld.db.meta import DBSession
from clld.db.models.common import ValueSet, Value, DomainElement, Parameter
from clld_phylogeny_plugin.interfaces import ITree
from clld_phylogeny_plugin.tree import Tree
from clld_glottologfamily_plugin.models import Family
from clldutils.misc import lazyproperty

from grambank import models


class GrambankTree(Tree):
    def __init__(self, *args, pids=None, **kw):
        self.pids = pids or []
        Tree.__init__(self, *args, **kw)

    @lazyproperty
    def parameters(self):
        if self.pids:
            return DBSession.query(Parameter) \
                .filter(Parameter.id.in_(self.pids)) \
                .options(
                joinedload_all(Parameter.valuesets, ValueSet.values),
                joinedload(Parameter.domain)) \
                .all()
        return []

    def get_marker(self, valueset):
        res = valueset.values[0].domainelement.jsondata['icon']
        return res[0], '#' + res[1:]


class GrambankGeoJsonParameter(GeoJsonParameter):
    def feature_iterator(self, ctx, req):
        de = req.params.get('domainelement')
        if de:
            query = DBSession.query(Value).join(DomainElement).filter(DomainElement.id == de)
            if ('family' in req.params) and req.params['family']:
                query = query\
                    .join(ValueSet)\
                    .join(ValueSet.language)\
                    .join(models.GrambankLanguage.family)\
                    .filter(Family.id == req.params['family'])
            return [
                v.valueset for v in query.options(
                    joinedload_all(Value.valueset, ValueSet.values),
                    joinedload(Value.valueset, ValueSet.language))]
        return self.get_query(ctx, req)


def includeme(config):
    config.registry.registerUtility(GrambankTree, ITree)
    config.register_adapter(
        GrambankGeoJsonParameter,
        interfaces.IParameter,
        name=GrambankGeoJsonParameter.mimetype)
