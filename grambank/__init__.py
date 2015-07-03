from clld.web.app import get_configurator, MapMarker
from clld.interfaces import IValue, IDomainElement, IMapMarker, IValueSet

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


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = get_configurator('grambank', (MyMapMarker(), IMapMarker), settings=settings)
    config.include('clldmpg')
    config.include('grambank.datatables')
    config.include('grambank.adapters')
    config.include('grambank.maps')
    return config.make_wsgi_app()
