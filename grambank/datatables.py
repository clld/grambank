from sqlalchemy.orm import aliased, joinedload, joinedload_all
from clld.db.util import get_distinct_values, icontains
from clld.web.util.helpers import map_marker_img
from clld.web.util.htmllib import HTML

from clld.db.models import common
from clld.web.datatables.base import Col, IdCol, LinkCol, DetailsRowLinkCol, LinkToMapCol, DataTable
from clld.web.datatables.value import Values, ValueNameCol
from clld.web.datatables.language import Languages
from clld.web.datatables.parameter import Parameters
from clld.web.datatables.contributor import Contributors, NameCol

from clld_glottologfamily_plugin.datatables import Familys, MacroareaCol, FamilyLinkCol, GlottologUrlCol
from clld_glottologfamily_plugin.models import Family

from models import GrambankLanguage, Feature, Dependency
from clld.web.util.helpers import link

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
    def __init__(self, req, *args, **kw):
        self.stability = kw.pop('stability', req.params.get('stability'))
        Parameters.__init__(self, req, *args, **kw)

#    def default_order(self):
#        return Feature.parsimony_stability_value descending TODO

    def xhr_query(self):
        res = Parameters.xhr_query(self)
        if self.stability:
            # make sure we can determine the stability table is requested also when called
            # via XHR.
            res['stability'] = '1'
        return res

    def col_defs(self):
        if self.stability:
            return [
                FeatureIdCol(self, 'Id', sClass='left', model_col=Feature.id),
                LinkCol(self, 'Feature', model_col=Feature.name),
                Col(self, 'Stability', model_col=Feature.parsimony_stability_value),
                Col(self, 'Retentions', model_col=Feature.parsimony_retentions),
                Col(self, 'Transitions', model_col=Feature.parsimony_transitions),
            ]

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

class Dependencies(DataTable):
    def default_order(self):
        return Dependency.strength

    def col_defs(self):
        return [
            IdCol(self, 'Id', sClass='left', model_col=Dependency.id),
            #LinkCol(self, 'From Feature', sClass='left', model_col=Dependency.f1),
            #LinkCol(self, 'To Feature', sClass='left', model_col=Dependency.f2),
            LinkCol(self, 'From Feature', sClass='left', model_col=Feature.name, get_object=lambda i: i.feature1),
            LinkCol(self, 'To Feature', sClass='left', model_col=Feature.name, get_object=lambda i: i.feature2),
            Col(self, 'Strength', model_col=Dependency.strength),
        ]


class LanguageCountCol(Col):
    __kw__ = {'bSearchable': False, 'bSortable': False}

    def format(self, item):
        return int(len(item.languages))

class FamilyMacroareaCol(Col):
    __kw__ = {'bSearchable': False, 'bSortable': False}

    def format(self, item):
        return ", ".join(set([lg.macroarea for lg in item.languages]))

    
class Families(Familys):    
    def col_defs(self):
        return [
            LinkCol(self, 'name'),
            GlottologUrlCol(self, 'description', sTitle='Glottolog'),
            FamilyMacroareaCol(self, 'macroarea'),
            LanguageCountCol(self, 'number of languages in GramBank'),
        ]

class GrambankContributionsCol(Col):
    __kw__ = {'bSearchable': False, 'bSortable': False}

    def format(self, item):
        return HTML.ul(
            *[HTML.li(link(
                self.dt.req, c.contribution, label="%s [%s]" % (c.contribution.desc, c.contribution.id))) for c in item.contribution_assocs])


class GrambankContributors(Contributors):
    def col_defs(self):
        return [
            NameCol(self, 'name'),
            GrambankContributionsCol(self, 'Contributions')
        ]

    
class Datapoints(Values):
    def base_query(self, query):
        query = Values.base_query(self, query)
        if self.language:
            query = query.options(
                joinedload_all(common.Value.valueset, common.ValueSet.parameter),
                joinedload(common.Value.domainelement),
            )
        return query

    def col_defs(self):
        name_col = ValueNameCol(self, 'value')
        if self.parameter and self.parameter.domain:
            name_col.choices = [(de.name, de.description) for de in self.parameter.domain]

        cols = []
        if self.parameter:
            cols = [
                LinkCol(
                    self, 'Name',
                    model_col=common.Language.name,
                    get_object=lambda i: i.valueset.language),
                Col(
                    self, 'ISO-639-3',
                    model_col=common.Language.id,
                    get_object=lambda i: i.valueset.language)]
        elif self.language:
            cols = [
                FeatureIdCol(
                    self, 'Feature Id',
                    sClass='left', model_col=common.Parameter.id,
                    get_object=lambda i: i.valueset.parameter),
                LinkCol(
                    self, 'Feature',
                    model_col=common.Parameter.name,
                    get_object=lambda i: i.valueset.parameter)
            ]

        cols = cols + [
            name_col,
            Col(self, 'Source',
                model_col=common.ValueSet.source,
                get_object=lambda i: i.valueset),
            Col(self, 'Comment', model_col=common.Value.description)
        ]
        return cols

    def get_options(self):
        if self.language or self.parameter:
            # if the table is restricted to the values for one language, the number of
            # features is an upper bound for the number of values; thus, we do not
            # paginate.
            return {'bLengthChange': False, 'bPaginate': False}


def includeme(config):
    config.register_datatable('values', Datapoints)
    config.register_datatable('languages', GrambankLanguages)
    config.register_datatable('parameters', Features)
    config.register_datatable('dependencys', Dependencies)
    config.register_datatable('contributors', GrambankContributors)
