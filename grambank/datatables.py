from sqlalchemy.orm import joinedload, joinedload_all
from clld.db.util import get_distinct_values
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

from grambank.models import GrambankLanguage, Feature, Coder
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
    def base_query(self, query):
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


class Features(Parameters):
    def col_defs(self):
        return [
            IdCol(self, 'Id', sClass='left', model_col=Feature.id),
            LinkCol(self, 'Feature', model_col=Feature.name),
            Col(self, 'patron', model_col=Feature.patron, choices=get_distinct_values(Feature.patron)),
            Col(self, 'Languages', model_col=Feature.representation),
            DetailsRowLinkCol(self, 'd', button_text='Values'),
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
            LanguageCountCol(self, 'number of languages in GramBank'),
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


class NCol(Col):
    def format(self, item):
        try:
            return '{0:,}'.format(int(Col.format(self, item)))
        except ValueError:
            return ''


class Coders(Contributors):
    def base_query(self, query):
        return query.options(joinedload_all(
            common.Contributor.contribution_assocs,
            common.ContributionContributor.contribution))

    def col_defs(self):
        return [
            NameCol(self, 'name'),
            NCol(self, 'datapoints', model_col=Coder.count_datapoints),
            GrambankContributionsCol(self, 'Contributions'),
        ]

    def get_options(self):
        return {'aaSorting': [[1, 'desc']]}


class Datapoints(Values):
    def base_query(self, query):
        query = Values.base_query(self, query)
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
    config.register_datatable('familys', Families)
    config.register_datatable('sources', References)
