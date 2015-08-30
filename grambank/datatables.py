from clld.db.util import get_distinct_values, icontains
from clld.web.util.helpers import map_marker_img
from clld.web.util.htmllib import HTML

from clld.web.datatables.base import Col, IdCol, LinkCol, DetailsRowLinkCol
from clld.web.datatables.language import Languages
from clld.web.datatables.parameter import Parameters

from models import GrambankLanguage, Family, Feature


class FeatureIdCol(IdCol):
    def search(self, qs):
        if self.model_col:
            return self.model_col.contains(qs)

    def order(self):
        return Feature.sortkey_str, Feature.sortkey_int


class FamilyCol(Col):
    def __init__(self, dt, name, **kw):
        kw['choices'] = get_distinct_values(Family.name)
        Col.__init__(self, dt, name, **kw)

    def order(self):
        return Family.name

    def search(self, qs):
        return icontains(Family.name, qs)

    def format(self, item):
        return HTML.div(map_marker_img(self.dt.req, item), ' ', item.family.name)


class GrambankLanguages(Languages):
    def base_query(self, query):
        return query.join(Family)

    def col_defs(self):
        res = Languages.col_defs(self)
        res.append(Col(self, 'macroarea', model_col=GrambankLanguage.macroarea))
        res.append(FamilyCol(self, 'family'))
        return res

class Features(Parameters):
    #def base_query(self, query):
    #    return query\
    #        .join(FeatureDomain).options(joinedload_all(Feature.featuredomain))

    def col_defs(self):
        return [
            FeatureIdCol(self, 'Id', sClass='left', model_col=Feature.id),
            LinkCol(self, 'Feature', model_col=Feature.name),
            #Col(self, 'Abbreviation', model_col=Feature.abbreviation),
            Col(self, 'Morphosynunit', model_col=Feature.jl_relevant_unit),
            Col(self, 'Form', model_col=Feature.jl_formal_means),
            Col(self, 'Function', model_col=Feature.jl_function),
            Col(self, 'Languages', model_col=Feature.representation),
            DetailsRowLinkCol(self, 'd', button_text='Values'),
        ]

    

def includeme(config):
    config.register_datatable('languages', GrambankLanguages)
    config.register_datatable('parameters', Features)
