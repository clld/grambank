from pyramid.config import Configurator

from clld.web.icon import MapMarker
from clld.interfaces import IValue, IDomainElement, IMapMarker, IValueSet, ILanguage

# we must make sure custom models are known at database initialization!
from grambank import models


class MyMapMarker(MapMarker):
    def get_icon(self, ctx, req):
        if IValue.providedBy(ctx):
            return ctx.domainelement.jsondata['icon']
        if IValueSet.providedBy(ctx):
            return ctx.values[0].domainelement.jsondata['icon']
        if IDomainElement.providedBy(ctx):
            return ctx.jsondata['icon']
        if ILanguage.providedBy(ctx):
            return ctx.family.icon


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('clldmpg')
    config.registry.registerUtility(MyMapMarker(), IMapMarker)
    return config.make_wsgi_app()
