"""
This module will be available in templates as ``u``.

This module is also used to lookup custom template context providers, i.e. functions
following a special naming convention which are called to update the template context
before rendering resource's detail or index views.
"""
from clld import RESOURCES
from clld.web.util.helpers import get_referents


def source_detail_html(context=None, request=None, **kw):
    return dict(referents=get_referents(context, exclude=[
        'language',
        'sentence',
        'contribution',
        #'valueset',
    ]))


def dataset_detail_html(context=None, request=None, **kw):
    return dict(stats=context.get_stats(
        [rsc for rsc in RESOURCES if rsc.name in ['language', 'parameter', 'value']]),
)