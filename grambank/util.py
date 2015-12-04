"""
This module will be available in templates as ``u``.

This module is also used to lookup custom template context providers, i.e. functions
following a special naming convention which are called to update the template context
before rendering resource's detail or index views.
"""
from sqlalchemy import func, desc, text

from clld import RESOURCES
from clld.web.util.helpers import get_referents
from clld.db.meta import DBSession
from clld.db.models.common import Contributor, ValueSet, Contribution, ContributionContributor


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

