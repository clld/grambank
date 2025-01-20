from sqlalchemy.orm import joinedload

from clld.db.util import icontains, get_distinct_values
from clld.web.util.htmllib import HTML, literal
from clld.web.util.helpers import map_marker_img
from clld.db.models import common
from clld.web.datatables.base import Col, IdCol, LinkCol, DetailsRowLinkCol, LinkToMapCol
from clld.web.datatables.value import Values, RefsCol
from clld.web.datatables.language import Languages
from clld.web.datatables.parameter import Parameters
from clld.web.datatables.contributor import Contributors, NameCol
from clld.web.datatables.source import Sources

from clld_glottologfamily_plugin.datatables import Familys, MacroareaCol, FamilyLinkCol, GlottologUrlCol
from clld_glottologfamily_plugin.models import Family

from grambank.models import GrambankLanguage, Feature
from clld.web.util.helpers import link


class ValueNameCol(LinkCol):

    """Render the label for a Value."""

    def get_obj(self, item):
        return item.valueset

    def get_attrs(self, item):
        label = str(item)
        title = label
        if self.dt.parameter:
            label = HTML.span(map_marker_img(self.dt.req, item), literal('&nbsp;'), label)
        return {'label': label, 'title': title}

    def order(self):
        return common.DomainElement.number \
            if self.dt.parameter and self.dt.parameter.domain \
            else common.Value.name

    def search(self, qs):
        if self.dt.parameter and self.dt.parameter.domain:
            return common.DomainElement.name.__eq__(qs)
        return icontains(common.Value.name, qs)


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
            Col(self, 'Features', model_col=GrambankLanguage.nzrepresentation),
        ]


class PatronCol(LinkCol):
    __kw__ = {'bSortable': False, 'bSearchable': False}

    def format(self, item):
        return ' and '.join([link(self.dt.req, p) for p in item.patrons])


class FeatureIdCol(IdCol):
    def search(self, qs):
        return icontains(Feature.id, qs)


class Features(Parameters):
    def base_query(self, query):
        return query.options(joinedload(Feature.contributor_assocs))

    def col_defs(self):
        return [
            FeatureIdCol(self, 'Id', sClass='left', model_col=Feature.id),
            LinkCol(self, 'Feature', model_col=Feature.name),
            PatronCol(self, 'patron', get_object=lambda i: i.patron),
            Col(self, 'Languages', model_col=Feature.nzrepresentation),
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
        return query.options(
            joinedload(common.Contributor.contribution_assocs)
            .joinedload(common.ContributionContributor.contribution))

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
        # NOTE:
        #  * self.parameter refers to a parameter in general
        #  * self.feature refers to a parameter specifically on the
        #    Family+Feature combination page
        self.feature = kw.pop('feature', None)
        if (not self.feature) and 'feature' in req.params:
            self.feature = common.Parameter.get(req.params['feature'], default=None)
        Values.__init__(self, req, *args, **kw)

    def base_query(self, query):
        query = query.join(common.Value.valueset)
        query = query.options(
            joinedload(common.Value.valueset)
            .joinedload(common.ValueSet.references)
            .joinedload(common.ValueSetReference.source))
        query = query.options(
            joinedload(common.Value.domainelement))

        if self.contribution:
            query = query.filter(common.ValueSet.contribution_pk == self.contribution.pk)

        query = query.join(common.ValueSet.language)
        if self.language:
            query = query.filter(common.ValueSet.language_pk == self.language.pk)

        if self.family:
            query = query.filter(GrambankLanguage.family_pk == self.family.pk)

        if self.parameter:
            query = query.filter(common.ValueSet.parameter_pk == self.parameter.pk)
            # only the parameter page shows language family
            query = query.outerjoin(GrambankLanguage.family)
            # only the parameter page shows contributors
            query = query.options(
                joinedload(common.Value.valueset)
                .joinedload(common.ValueSet.contribution)
                .joinedload(common.Contribution.contributor_assocs)
                .joinedload(common.ContributionContributor.contributor))
            # also, we need to explicitly join in the contributors as well,
            # otherwise the search box won't work
            query = query\
                .join(common.ValueSet.contribution)\
                .join(common.Contribution.contributor_assocs)\
                .join(common.ContributionContributor.contributor)
            # due to the contributor join above, every datapoint with multiple
            # contributors will show up multiple times, so we need to squash
            # them back together
            query = query.distinct()
        elif self.feature:
            query = query.filter(common.ValueSet.parameter_pk == int(self.feature.pk))
        else:
            query = query.join(common.ValueSet.parameter)

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
                FamilyLinkCol(
                    self, 'Family', GrambankLanguage,
                    get_object=lambda i: i.valueset.language,
                ),
                Col(
                    self, 'Macroarea',
                    model_col=GrambankLanguage.macroarea,
                    get_object=lambda i: i.valueset.language,
                    choices=get_distinct_values(GrambankLanguage.macroarea),
                ),
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
            #Col(self, 'name', sTitle='Value'),
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
