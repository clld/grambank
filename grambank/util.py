"""
This module will be available in templates as ``u``.

This module is also used to lookup custom template context providers, i.e. functions
following a special naming convention which are called to update the template context
before rendering resource's detail or index views.
"""
import re
import itertools
import collections

from sqlalchemy import func, desc, text
from sqlalchemy.orm import joinedload

from clld import RESOURCES
from clld.web.util.helpers import get_referents
from clld.web.util.htmllib import HTML
from clld.db.meta import DBSession
from clld.db.models.common import (
    Contributor, ValueSet, Contribution, ContributionContributor, Language, Parameter, Value,
)
from clld_glottologfamily_plugin.models import Family
from clld.web.util.multiselect import CombinationMultiSelect
from clld.web.icon import Icon
from clld.web.util import glottolog  # used in templates!
from clld_phylogeny_plugin.models import Phylogeny
from clldutils.misc import slug
from markdown import markdown

from grambank.models import GrambankLanguage, DatapointContributor, Datapoint

COLORS = [
    #            red     yellow
    "00ff00", "ff0000", "ffff00", "0000ff", "ff00ff", "00ffff", "000000",
]
assert markdown


def icon_from_req(ctx, req):
    return Icon.from_req(
        ctx,
        req,
        icon_map={
            'cffffff': 'c0077bb',
            'cff0000': 'ccc3311',
            'c0000ff': 'c009988',
            'cffff00': 'cee7733',
        })


def process_markdown(text, req, section=None):
    from markdown import markdown

    md, in_section, current_section = [], False, None
    in_example = False
    for i, line in enumerate(text.strip().split('\n'), start=1):
        if line.startswith('##'):
            current_section = line[2:].strip()
            line = '##' + line
            if current_section.startswith('Patron'):
                break
        if section and current_section != section:
            in_section = False
        if i == 1 and line.startswith('##'):
            continue
        if line.startswith('```'):
            in_example = not in_example
        elif in_example:
            line = line.lstrip()
        if (not section) or in_section:
            md.append(line)
        if section and current_section == section:
            in_section = True

    html = markdown('\n'.join(md), extensions=['tables', 'fenced_code', 'toc'])
    wiki_url_pattern = re.compile('https://github.com/grambank/[gG]rambank/wiki/(?P<id>GB[0-9]{3})')
    html = wiki_url_pattern.sub(lambda m: req.route_url('parameter', id=m.group('id')), html)
    return html.replace('<code>', '').replace('</code>', '').replace('<table>', '<table class="table table-nonfluid">')


def contributor_index_html(request=None, context=None, **kw):
    contribs = DBSession.query(Contributor).all()

    ndatapoint = {r[0]: r[1] for r in DBSession.query(
        DatapointContributor.contributor_pk, func.count(DatapointContributor.datapoint_pk)).group_by(DatapointContributor.contributor_pk)}
    nlangs = {r[0]: r[1] for r in DBSession.query(
        ContributionContributor.contributor_pk, func.count(ContributionContributor.contribution_pk)).group_by(ContributionContributor.contributor_pk)}

    res = []
    for role, plural in [
        ('Project leader', None),
        ('Senior advisor', 'Senior advisors'),
        ('Project coordinator', None),
        ('Database managers', None),
        ('Patron', 'Patrons'),
        ('Node leader', 'Node leaders'),
        ('Coder', 'Coders'),
        ('Methods-team', None),
    ]:
        cs = sorted([c for c in contribs if role in c.jsondata['roles']], key=lambda cc: cc.name.split()[-1])
        iter_ = iter(cs)
        people = list(itertools.zip_longest(iter_, iter_, iter_, iter_))
        res.append((plural or role, slug(role), people))

    return dict(contribs=res, ndatapoint=ndatapoint, nlangs=nlangs)


def family_detail_html(request=None, context=None, **kw):
    return {
        'features': DBSession.query(Parameter).all(),
        'feature': Parameter.get(request.params['feature']) if request.params.get('feature') else None,
        'phylogeny': Phylogeny.get(context.id, default=None),
    }


def phylogeny_detail_html(request=None, context=None, **kw):
    return {
        'ms': CombinationMultiSelect,
    }


def source_detail_html(context=None, request=None, **kw):
    return dict(referents=get_referents(context, exclude=[
        'sentence',
        'contribution',
        'valueset',
    ]))


def contributor_detail_html(context=None, request=None, **kw):
    counts = {r[0]: r[1] for r in DBSession.query(Datapoint.language_pk, func.count(DatapointContributor.pk))\
        .join(DatapointContributor)\
        .filter(DatapointContributor.contributor_pk == context.pk)\
        .group_by(Datapoint.language_pk)}
    languages = []
    for lang in DBSession.query(Language) \
            .outerjoin(Family) \
            .join(ValueSet) \
            .join(Contribution) \
            .join(ContributionContributor) \
            .filter(Language.pk.in_(list(counts.keys()))) \
            .order_by(Family.name, Language.name) \
            .options(joinedload(GrambankLanguage.family)):
        languages.append((lang, counts[lang.pk]))
    return {'languages': languages}


def dataset_detail_html(context=None, request=None, **kw):
    contribs = DBSession.query(Contributor.name, func.count(ValueSet.id).label('c'))\
        .join(
            Contributor.contribution_assocs,
            ContributionContributor.contribution,
            Contribution.valuesets)\
        .group_by(Contributor.name)\
        .order_by(desc(text('c')))
    return dict(
        contribs=contribs,
        stats=context.get_stats(
            [rsc for rsc in RESOURCES if rsc.name in ['language', 'parameter', 'value']]),
        nzvalues=DBSession.query(Value).filter(Value.name != '?').count(),
    )
