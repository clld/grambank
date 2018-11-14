from pyramid.config import Configurator

from clld.interfaces import (
    IValue, IDomainElement, IMapMarker, IValueSet, ILinkAttrs, IContribution,
)
from clld_glottologfamily_plugin.util import LanguageByFamilyMapMarker

# we must make sure custom models are known at database initialization!
from grambank import models
from grambank import views


_ = lambda s: s
_('Parameters')
_('Parameter')
_('Familys')


class MyMapMarker(LanguageByFamilyMapMarker):
    def get_icon(self, ctx, req):
        if IValue.providedBy(ctx):
            return ctx.domainelement.jsondata['icon']
        if IValueSet.providedBy(ctx):
            return ctx.values[0].domainelement.jsondata['icon']
        if IDomainElement.providedBy(ctx):
            return ctx.jsondata['icon']
        return LanguageByFamilyMapMarker.get_icon(self, ctx, req)


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
    
    config.registry.settings['home_comp'].append('coverage')
    config.add_route('coverage', pattern='/coverage')
    config.add_view(views.coverage, route_name='coverage', renderer='coverage.mako')

    config.registry.registerUtility(MyMapMarker(), IMapMarker)
    config.registry.registerUtility(link_attrs, ILinkAttrs)
    return config.make_wsgi_app()
