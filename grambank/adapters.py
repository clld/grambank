from sqlalchemy.orm import joinedload, joinedload_all

from clld import interfaces
from clld.web.adapters.geojson import GeoJsonParameter
from clld.db.meta import DBSession
from clld.db.models.common import ValueSet, Value, DomainElement


class GrambankGeoJsonParameter(GeoJsonParameter):
    def feature_iterator(self, ctx, req):
        de = req.params.get('domainelement')
        if de:
            return [
                v.valueset for v in DBSession.query(Value)
                .join(DomainElement)
                .filter(DomainElement.id == de)
                .options(
                    joinedload_all(Value.valueset, ValueSet.values),
                    joinedload(Value.valueset, ValueSet.language))]
        return self.get_query(ctx, req)


def includeme(config):
    config.register_adapter(
        GrambankGeoJsonParameter,
        interfaces.IParameter,
        name=GrambankGeoJsonParameter.mimetype)
