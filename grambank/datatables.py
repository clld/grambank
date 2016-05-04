from sqlalchemy.orm import aliased, joinedload, joinedload_all
from clld.db.util import get_distinct_values, icontains
from clld.web.util.htmllib import HTML

from clld.db.models import common
from clld.web.datatables.base import Col, IdCol, LinkCol, DetailsRowLinkCol, LinkToMapCol, DataTable
from clld.web.datatables.value import Values, ValueNameCol
from clld.web.datatables.language import Languages
from clld.web.datatables.parameter import Parameters
from clld.web.datatables.contributor import Contributors, NameCol

from clld_glottologfamily_plugin.datatables import Familys, MacroareaCol, FamilyLinkCol, GlottologUrlCol
from clld_glottologfamily_plugin.models import Family

from models import GrambankLanguage, Feature, Dependency, Transition, Stability, DeepFamily, Support, HasSupport
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

class Stabilities(DataTable):
    def get_options(self):
        opts = super(Stabilities, self).get_options()
        opts['aaSorting'] = [[2, 'desc']]
        return opts
    
    def base_query(self, query):
        return query.outerjoin(Feature)

    def col_defs(self):
        return [
            FeatureIdCol(self, 'Id', sClass='left', model_col=Stability.id),
            LinkCol(self, 'Feature', model_col=Feature.name, get_object=lambda i: i.feature),
            Col(self, 'Stability', model_col=Stability.parsimony_stability_value),
            Col(self, 'Retentions', model_col=Stability.parsimony_retentions),
            Col(self, 'Transitions', model_col=Stability.parsimony_transitions),
        ]
    
class Features(Parameters):
    #def __init__(self, req, *args, **kw):
    #    self.stability = kw.pop('stability', req.params.get('stability'))
    #    Parameters.__init__(self, req, *args, **kw)

    #def xhr_query(self):
    #    res = Parameters.xhr_query(self)
    #    if self.stability:
    #        # make sure we can determine the stability table is requested also when called
    #        # via XHR.
    #        res['stability'] = '1'
    #    return res

    def col_defs(self):
        #if self.stability:
        #    return [
        #        FeatureIdCol(self, 'Id', sClass='left', model_col=Feature.id),
        #        LinkCol(self, 'Feature', model_col=Feature.name),
        #        Col(self, 'Stability', model_col=Feature.parsimony_stability_value),
        #        Col(self, 'Retentions', model_col=Feature.parsimony_retentions),
        #        Col(self, 'Transitions', model_col=Feature.parsimony_transitions),
        #    ]

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
    def __init__(self, req, model, **kw):
        DataTable.__init__(self, req, model, **kw)
        self.f1 = aliased(Feature, name="f1")
        self.f2 = aliased(Feature, name="f2")

    def base_query(self, query):
        query = query\
            .join(self.f1, self.f1.pk == Dependency.feature1_pk)\
            .options(joinedload(Dependency.feature1))\
            .join(self.f2, self.f2.pk == Dependency.feature2_pk)\
            .options(joinedload(Dependency.feature2))
        return query

    def get_options(self):
        opts = super(Dependencies, self).get_options()
        opts['aaSorting'] = [[3, 'desc'], [4, 'desc']]
        return opts

    def col_defs(self):
        return [
            IdCol(self, 'Id', sClass='left', model_col=Dependency.id),
            #LinkCol(self, 'From Feature', sClass='left', model_col=Dependency.f1),
            #LinkCol(self, 'To Feature', sClass='left', model_col=Dependency.f2),
            LinkCol(self, 'From Feature', sClass='left', model_col=self.f1.name, get_object=lambda i: i.feature1),
            LinkCol(self, 'To Feature', sClass='left', model_col=self.f2.name, get_object=lambda i: i.feature2),
            Col(self, 'Strength', model_col=Dependency.strength),
            Col(self, 'Representation', model_col=Dependency.representation),
            StatusCol(self, 'Status', Dependency, attribute = "combinatory_status"),
        ]
    
class Transitions(DataTable):
    __constraints__ = [Stability]

    def base_query(self, query):
        query = query.outerjoin(Stability).outerjoin(Family)
        if self.stability:
            query = query.filter(Transition.stability_pk == self.stability.pk)
        return query
    
    def col_defs(self):
        return [
            IdCol(self, 'Id', sClass='left', model_col=Transition.id),
            LinkCol(self, 'Feature', sClass='left', model_col=Stability.id, get_object=lambda i: i.stability),
            FamilyLinkCol(self, 'Family', Transition),
            Col(self, 'From Node', model_col=Transition.fromnode),
            Col(self, 'From Value', model_col=Transition.fromvalue),
            Col(self, 'To Node', model_col=Transition.tonode),
            Col(self, 'To Value', model_col=Transition.tovalue),
            StatusCol(self, 'Retention/Innovation', Transition, attribute = "retention_innovation"),
        ]

class Supports(DataTable):
    __constraints__ = [HasSupport, DeepFamily]

    def base_query(self, query):
        query = query.outerjoin(HasSupport).outerjoin(DeepFamily).outerjoin(Feature)
        if self.deepfamily:
            query = query.filter(HasSupport.deepfamily_pk == self.deepfamily.pk)
        return query

    def get_options(self):
        opts = super(Supports, self).get_options()
        opts['aaSorting'] = [[3, 'desc'], [4, 'desc'], [5, 'desc']]
        return opts

    def col_defs(self):
        return [
            #IdCol(self, 'Id', sClass='left', model_col=Support.id),
            LinkCol(self, 'Feature', model_col=Feature.name, get_object=lambda i: i.feature),
            Col(self, 'Value 1', model_col=Support.value1),
            Col(self, 'Value 2', model_col=Support.value2),
            Col(self, 'Support Score', model_col=Support.support_score),
            Col(self, 'Historical Score', model_col=Support.historical_score),
            Col(self, 'Independent Score', model_col=Support.independent_score),
        ]


    
class DeepFamilies(DataTable):
    def __init__(self, req, model, **kw):
        DataTable.__init__(self, req, model, **kw)
        self.fam1 = aliased(Family, name="fam1")
        self.fam2 = aliased(Family, name="fam2")

    def base_query(self, query):
        query = query\
            .join(self.fam1, self.fam1.pk == DeepFamily.family1_pk)\
            .options(joinedload(DeepFamily.family1))\
            .join(self.fam2, self.fam2.pk == DeepFamily.family2_pk)\
            .options(joinedload(DeepFamily.family2))
        return query

    def get_options(self):
        opts = super(DeepFamilies, self).get_options()
        opts['aaSorting'] = [[3, 'desc'], [4, 'desc']]
        return opts

    def col_defs(self):
        return [
            IdCol(self, 'Id', sClass='left', model_col=DeepFamily.id),
            LinkCol(self, 'Family 1', sClass='left', model_col=self.fam1.name, get_object=lambda i: i.family1),
            LinkCol(self, 'Family 2', sClass='left', model_col=self.fam2.name, get_object=lambda i: i.family2),
            Col(self, 'Support Value', model_col=DeepFamily.support_value),
            Col(self, 'Significance', model_col=DeepFamily.significance),
            Col(self, 'Distance (km)', model_col=DeepFamily.geographic_plausibility),
        ]

    
class StatusCol(Col):
    def __init__(self, dt, name, cls, attribute = 'combinatory_status', **kw):
        self._col = getattr(cls, attribute)
        self.attribute = attribute
        kw['choices'] = get_distinct_values(self._col)
        Col.__init__(self, dt, name, **kw)

    def order(self):
        return self._col

    def search(self, qs):
        return icontains(self._col, qs)

    def format(self, item):
        return getattr(self.get_obj(item), self.attribute)
    
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
    config.register_datatable('transitions', Transitions)
    config.register_datatable('stabilitys', Stabilities)
    config.register_datatable('deepfamilys', DeepFamilies)
    config.register_datatable('supports', Supports)
