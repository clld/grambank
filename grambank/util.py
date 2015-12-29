"""
This module will be available in templates as ``u``.

This module is also used to lookup custom template context providers, i.e. functions
following a special naming convention which are called to update the template context
before rendering resource's detail or index views.
"""
from __future__ import division, unicode_literals

from sqlalchemy import func, desc, text

from clld import RESOURCES
from clld.web.util.helpers import get_referents
from clld.web.util.htmllib import HTML
from clld.db.meta import DBSession
from clld.db.models.common import Contributor, ValueSet, Contribution, ContributionContributor
from models import Dependency

def td_coverage(glottolog=0, grambank=0, label=None):
    style = ''
    if glottolog == 0:
        style = 'background-color: hsl(120,100%,50%)'
        if grambank == 0:
            percentage = 0
        else:
            percentage = 1
    else:
        percentage = grambank / glottolog
    return HTML.td(
        label if label else '\xa0%s%%\xa0' % int(round(percentage * 100)),
        class_='left' if label else 'center',
        style=style or 'background-color: hsl({0},100%,50%)'.format((percentage) * 120))


def source_detail_html(context=None, request=None, **kw):
    return dict(referents=get_referents(context, exclude=[
        'language',
        'sentence',
        'contribution',
        #'valueset',
    ]))


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
    )

def combination_detail_html(context=None, request=None, **kw):
    [f1, f2] = context.parameters[:2]
    [dependency] = list(DBSession.query(Dependency).filter(Dependency.feature1_pk == f1.pk, Dependency.feature2_pk == f2.pk))
    r = dependency.jsondata
    r["f1id"] = f1.id
    r["f2id"] = f2.id
    r["f1f2id"] = dependency.id
    r["strength"] = dependency.strength if r["f2h"] > 0.0 else "-"
    r["combinatory_status"] = dependency.combinatory_status
    return {'dependency': r}
