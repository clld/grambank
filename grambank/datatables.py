from clld.db.util import get_distinct_values, icontains
from clld.web.util.helpers import map_marker_img
from clld.web.util.htmllib import HTML

from clld.web.datatables.base import Col, IdCol, LinkCol, DetailsRowLinkCol, LinkToMapCol
from clld.web.datatables.language import Languages
from clld.web.datatables.parameter import Parameters

from clld_glottologfamily_plugin.datatables import MacroareaCol, FamilyLinkCol
from clld_glottologfamily_plugin.models import Family

from models import GrambankLanguage, Feature


class FeatureIdCol(IdCol):
    def search(self, qs):
        if self.model_col:
            return self.model_col.contains(qs)

    def order(self):
        return Feature.sortkey_str, Feature.sortkey_int


class LanguageIdCol(LinkCol):
    def get_attrs(self, item):
        return dict(label=item.id)


class GrambankLanguages(Languages):
    def base_query(self, query):
        return query.outerjoin(Family)

    def col_defs(self):
        return [
            LanguageIdCol(self, 'id'),
            LinkCol(self, 'name'),
            LinkToMapCol(self, 'm'),
            Col(self,
                'latitude',
                sDescription='<small>The geographic latitude</small>'),
            Col(self,
                'longitude',
                sDescription='<small>The geographic longitude</small>'),
            MacroareaCol(self, 'macroarea', GrambankLanguage),
            FamilyLinkCol(self, 'family', GrambankLanguage),
        ]


class Features(Parameters):
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
