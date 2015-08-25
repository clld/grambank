from pyramid.config import Configurator
from functools import partial

from clld.web.icon import MapMarker
from clld.interfaces import IParameter, IValue, IDomainElement, IMapMarker, IValueSet, ILanguage
from clld.web.adapters.base import adapter_factory
from clld.web.app import menu_item

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
    config.register_menu(
        ('dataset', partial(menu_item, 'dataset', label='Home')),
        ('parameters', partial(menu_item, 'parameters', label='Features')),
        ('languages', partial(menu_item, 'languages')),
        ('sources', partial(menu_item, 'sources')),
    )

    config.include('clldmpg')
    config.include('grambank.adapters')
    config.include('grambank.datatables')
    config.include('grambank.maps')

    config.register_adapter(adapter_factory(
        'parameter/detail_tab.mako',
        mimetype='application/vnd.clld.tab',
        send_mimetype="text/plain",
        extension='tab',
        name='tab-separated values'), IParameter)


    return config.make_wsgi_app()
