import functools

from pyramid.config import Configurator
from sqlalchemy.orm import joinedload

from clld.interfaces import (
    IValue, IDomainElement, IMapMarker, IValueSet, ILinkAttrs, IContribution, ICtxFactoryQuery,
)
from clld.web.app import CtxFactoryQuery, menu_item
from clld_glottologfamily_plugin.util import LanguageByFamilyMapMarker
from clld.db.models import common
from clldutils import svg

# we must make sure custom models are known at database initialization!
from grambank import models
from grambank import views
from grambank import datatables

_ = lambda s: s
_('Parameters')
_('Parameter')
_('Familys')
_('Languages')


class GrambankMapMarker(LanguageByFamilyMapMarker):
    def __call__(self, ctx, req):
        if IValue.providedBy(ctx):
            icon = ctx.domainelement.jsondata['icon']
        elif IValueSet.providedBy(ctx):
            icon = ctx.values[0].domainelement.jsondata['icon']
        elif IDomainElement.providedBy(ctx):
            icon = ctx.jsondata['icon']
        else:
            icon = LanguageByFamilyMapMarker.get_icon(self, ctx, req)
        icon = {
            'cffffff': 'c0077bb',
            'cff0000': 'ccc3311',
            'c0000ff': 'c009988',
            'cffff00': 'cee7733',
        }.get(icon, icon)
        return svg.data_url(svg.icon(icon, opacity=0.8))


class GrambankCtxFactoryQuery(CtxFactoryQuery):
    def refined_query(self, query, model, req):
        if model == common.Language:
            query = query.options(joinedload(models.GrambankLanguage.family))
        return query


def link_attrs(req, obj, **kw):
    if IContribution.providedBy(obj):
        # we are about to link to a contribution details page: redirect to language page!
        kw['href'] = req.route_url('language', id=obj.id, **kw.pop('url_kw', {}))

    return kw


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('clldmpg')
    config.include('clld_glottologfamily_plugin')
    config.include('clld_phylogeny_plugin')
    config.register_datatable('familys', datatables.Families)
    config.add_route_and_view('faq', '/faq', lambda *args, **kw: {}, renderer='faq.mako')

    config.registry.registerUtility(GrambankCtxFactoryQuery(), ICtxFactoryQuery)
    config.registry.registerUtility(GrambankMapMarker(), IMapMarker)
    config.registry.registerUtility(link_attrs, ILinkAttrs)

    config.register_menu(
        ('dataset', functools.partial(menu_item, 'dataset', label='Home')),
        ('parameters', functools.partial(menu_item, 'parameters', label='Features')),
        ('languages', functools.partial(menu_item, 'languages', label='Languages and dialects')),
        ('contributors', functools.partial(menu_item, 'contributors', label='People')),
        ('faq', functools.partial(menu_item, 'faq', label='FAQ')),
    )

    return config.make_wsgi_app()
