from pyramid.config import Configurator

from clld.interfaces import IValue, IDomainElement, IMapMarker, IValueSet

from clld_glottologfamily_plugin.util import LanguageByFamilyMapMarker

# we must make sure custom models are known at database initialization!
from grambank import models
from grambank import views


class MyMapMarker(LanguageByFamilyMapMarker):
    def get_icon(self, ctx, req):
        if IValue.providedBy(ctx):
            return ctx.domainelement.jsondata['icon']
        if IValueSet.providedBy(ctx):
            return ctx.values[0].domainelement.jsondata['icon']
        if IDomainElement.providedBy(ctx):
            return ctx.jsondata['icon']
        return LanguageByFamilyMapMarker.get_icon(self, ctx, req)


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('clldmpg')
    config.include('clld_glottologfamily_plugin')
    
    config.registry.settings['home_comp'].append('coverage')
    config.add_route('coverage', pattern='/coverage')
    config.add_view(views.coverage, route_name='coverage', renderer='coverage.mako')

    config.registry.settings['home_comp'].append('stability')
    config.add_route('stability', pattern='/stability')
    config.add_view(views.stability, route_name='stability', renderer='stability.mako')

    config.registry.settings['home_comp'].append('dependencies')
    config.add_route('dependencies', pattern='/dependencies')
    config.add_view(views.dependencies, route_name='dependencies', renderer='dependencies.mako')
    
    config.registry.registerUtility(MyMapMarker(), IMapMarker)
    return config.make_wsgi_app()
