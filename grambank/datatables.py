from sqlalchemy.orm import joinedload, joinedload_all

from clld.db.meta import DBSession
from clld.db.util import icontains, get_distinct_values
from clld.web.util.htmllib import HTML
from clld.db.models import common
from clld.web.datatables.base import Col, IdCol, LinkCol, DetailsRowLinkCol, LinkToMapCol
from clld.web.datatables.value import Values, ValueNameCol, RefsCol
from clld.web.datatables.language import Languages
from clld.web.datatables.parameter import Parameters
from clld.web.datatables.contributor import Contributors, NameCol
from clld.web.datatables.source import Sources

from clld_glottologfamily_plugin.datatables import Familys, MacroareaCol, FamilyLinkCol, GlottologUrlCol
from clld_glottologfamily_plugin.models import Family

from grambank.models import GrambankLanguage, Feature
from clld.web.util.helpers import link


class LanguagesCol(Col):
    __kw__ = dict(bSortable=False, bSearchable=False)

    def format(self, item):
        return HTML.ul(
            *[HTML.li(link(self.dt.req, lang)) for lang in item.languages],
            class_='unstyled')


class References(Sources):
    def col_defs(self):
        res = Sources.col_defs(self)[:-1]
        res.append(LanguagesCol(self, 'languages'))
        return res


class LanguageIdCol(LinkCol):
    def get_attrs(self, item):
        return dict(label=item.id)


class GrambankLanguages(Languages):
    __constraints__ = [Family]

    def base_query(self, query):
        if self.family:
            return query.join(Family).filter(GrambankLanguage.family == self.family).options(joinedload(GrambankLanguage.family))
        return query.outerjoin(Family).options(joinedload(GrambankLanguage.family))

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
            Col(self, 'Features', model_col=GrambankLanguage.representation),
        ]


class PatronCol(LinkCol):
    def __init__(self, *args, **kw):
        kw['choices'] = [
            c.name for c in DBSession.query(common.Contributor).filter(
                common.Contributor.pk.in_(DBSession.query(Feature.patron_pk)))]
        LinkCol.__init__(self, *args, **kw)

    def order(self):
        return common.Contributor.name

    def search(self, qs):
        return qs == common.Contributor.name


class FeatureIdCol(IdCol):
    def search(self, qs):
        return icontains(Feature.id, qs)


class Features(Parameters):
    def base_query(self, query):
        return query.join(common.Contributor).options(joinedload(Feature.patron))

    def col_defs(self):
        return [
            FeatureIdCol(self, 'Id', sClass='left', model_col=Feature.id),
            LinkCol(self, 'Feature', model_col=Feature.name),
            PatronCol(self, 'patron', get_object=lambda i: i.patron),
            Col(self, 'Languages', model_col=Feature.representation),
            DetailsRowLinkCol(self, 'd', button_text='Values and description'),
        ]


class LanguageCountCol(Col):
    __kw__ = {'bSearchable': False, 'bSortable': False}

    def format(self, item):
        return int(len(item.languages))


class FamilyMacroareaCol(Col):
    __kw__ = {'bSearchable': False, 'bSortable': False}

    def format(self, item):
        return ", ".join(set([lg.macroarea or "" for lg in item.languages]))

    
class Families(Familys):    
    def col_defs(self):
        return [
            LinkCol(self, 'name'),
            GlottologUrlCol(self, 'description', sTitle='Glottolog'),
            FamilyMacroareaCol(self, 'macroarea'),
            LanguageCountCol(
                self,
                'number of languages in GramBank',
                sClass='right'),
        ]


class GrambankContributionsCol(Col):
    __kw__ = {'bSearchable': False, 'bSortable': False}

    def format(self, item):
        return HTML.div(
            HTML.div(
                HTML.div(
                    HTML.a(
                        '{0} Languages'.format(len(item.contribution_assocs)),
                        **{'class': 'accordion-toggle',
                           'data-toggle': 'collapse',
                           'data-parent': '#acc-{0}'.format(item.pk),
                           'href': '#coll-{0}'.format(item.pk)}
                    ),
                    class_='accordion-heading'
                ),
                HTML.div(
                    HTML.div(
                        HTML.ul(
                            *[HTML.li(link(
                                self.dt.req, c.contribution)) for c in item.contribution_assocs]),
                        class_='accordion-inner'
                    ),
                    **{'class': 'accordion-body collapse',
                       'id': 'coll-{0}'.format(item.pk)}
                ),
                class_='accordion-group',
            ),
            class_='accordion',
            id='acc-{0}'.format(item.pk)
        )


class Coders(Contributors):
    def base_query(self, query):
        return query.options(joinedload_all(
            common.Contributor.contribution_assocs,
            common.ContributionContributor.contribution))

    def col_defs(self):
        return [
            NameCol(self, 'name'),
            GrambankContributionsCol(self, 'Contributions'),
        ]

    def get_options(self):
        return {'aaSorting': [[1, 'desc']]}


class Datapoints(Values):
    __constraints__ = [common.Parameter, common.Contribution, common.Language, Family]

    def __init__(self, req, *args, **kw):
        self.feature = kw.pop('feature', None)
        if (not self.feature) and 'feature' in req.params:
            self.feature = common.Parameter.get(req.params['feature'])
        Values.__init__(self, req, *args, **kw)

    def base_query(self, query):
        query = Values.base_query(self, query)
        if self.family:
            if self.feature:
                query = query.filter(common.ValueSet.parameter_pk == int(self.feature.pk))
            query = query.join(GrambankLanguage).join(Family).filter(GrambankLanguage.family == self.family)
            query = query.options(
                joinedload_all(common.Value.valueset, common.ValueSet.parameter),
                joinedload(common.Value.domainelement),
            )
        else:
            if self.language:
                query = query.options(
                    joinedload_all(common.Value.valueset, common.ValueSet.parameter),
                    joinedload(common.Value.domainelement),
                )
            if self.parameter:
                query = query\
                    .join(common.ValueSet.contribution)\
                    .join(common.Contribution.contributor_assocs)\
                    .join(common.ContributionContributor.contributor)\
                    .options(
                    joinedload(common.Value.valueset, common.ValueSet.language),
                    joinedload_all(
                        common.Value.valueset,
                        common.ValueSet.contribution,
                        common.Contribution.contributor_assocs,
                        common.ContributionContributor.contributor))
        return query

    def xhr_query(self):
        res = Values.xhr_query(self)
        if self.feature:
            res['feature'] = self.feature.id
        return res

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
                    self, 'Glottocode',
                    model_col=common.Language.id,
                    get_object=lambda i: i.valueset.language),
                LinkCol(
                    self, 'Contributor',
                    model_col=common.Contributor.name,
                    get_object=lambda i: i.valueset.contribution.contributor_assocs[0].contributor,
                )
            ]
        elif self.language:
            cols = [
                IdCol(
                    self, 'Feature Id',
                    sClass='left', model_col=common.Parameter.id,
                    get_object=lambda i: i.valueset.parameter),
                LinkCol(
                    self, 'Feature',
                    model_col=common.Parameter.name,
                    get_object=lambda i: i.valueset.parameter)
            ]
        elif self.family:
            cols = [
                LinkCol(
                    self, 'Name',
                    model_col=common.Language.name,
                    get_object=lambda i: i.valueset.language)
            ]
            if not self.feature:
                cols.extend([
                    IdCol(
                        self, 'Feature Id',
                        sClass='left', model_col=common.Parameter.id,
                        get_object=lambda i: i.valueset.parameter),
                    LinkCol(
                        self, 'Feature',
                        model_col=common.Parameter.name,
                        get_object=lambda i: i.valueset.parameter,
                        choices=get_distinct_values(common.Parameter.name),
                    )
                ])

        cols = cols + [
            name_col,
            RefsCol(self, 'Source',
                model_col=common.ValueSet.source,
                get_object=lambda i: i.valueset),
            Col(self, 'Comment', model_col=common.Value.description),
            #Col(self, 'Contributed By', model_col=common.Contribution.name,
            #        get_object=lambda i: i.valueset.contribution)
 
        ]
        return cols

    def get_options(self):
        if self.language:
            # if the table is restricted to the values for one language, the number of
            # features is an upper bound for the number of values; thus, we do not
            # paginate.
            return {'bLengthChange': False, 'bPaginate': False}
        return {}


def includeme(config):
    config.register_datatable('values', Datapoints)
    config.register_datatable('languages', GrambankLanguages)
    config.register_datatable('parameters', Features)
    config.register_datatable('contributors', Coders)
    config.register_datatable('sources', References)
