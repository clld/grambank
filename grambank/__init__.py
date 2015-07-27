from pyramid.config import Configurator

from clld.interfaces import IParameter, IValue, IDomainElement, IMapMarker, IValueSet, ILanguage
from clld.web.adapters.base import adapter_factory
from clld_glottologfamily_plugin.util import LanguageByFamilyMapMarker

# we must make sure custom models are known at database initialization!
from grambank import models


class MyMapMarker(LanguageByFamilyMapMarker):
    def get_icon(self, ctx, req):
        if IValue.providedBy(ctx):
            return ctx.domainelement.jsondata['icon']
        if IValueSet.providedBy(ctx):
            return ctx.values[0].domainelement.jsondata['icon']
        if IDomainElement.providedBy(ctx):
            return ctx.jsondata['icon']
        return super(MyMapMarker, self).get_icon(ctx, req)


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('clldmpg')
    config.registry.registerUtility(MyMapMarker(), IMapMarker)
    config.register_adapter(adapter_factory(
        'parameter/detail_tab.mako',
        mimetype='application/vnd.clld.tab',
        send_mimetype="text/plain",
        extension='tab',
        name='tab-separated values'), IParameter)
    return config.make_wsgi_app()
