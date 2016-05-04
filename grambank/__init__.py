from pyramid.config import Configurator

from clld.interfaces import IValue, IDomainElement, IMapMarker, IValueSet, ILinkAttrs
from clld_glottologfamily_plugin.util import LanguageByFamilyMapMarker

# we must make sure custom models are known at database initialization!
from grambank import models
from grambank import views
from grambank.interfaces import IDependency, ITransition, IStability, IDeepFamily, ISupport
from grambank.models import Dependency, Transition, Stability, DeepFamily, Support
from grambank.datatables import Families


_ = lambda s: s
_('Parameters')
_('Parameter')
_('Familys')
_('Dependencys')
_('Stabilitys')
_('Deepfamilys')


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
    if IDependency.providedBy(obj):
        # we are about to link to a dependency details page: redirect to combination page!
        id_ = obj.id.replace("->", "_")
        kw['href'] = req.route_url('combination', id=id_, **kw.pop('url_kw', {}))
    return kw

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('clldmpg')
    config.include('clld_glottologfamily_plugin')
    
    config.registry.settings['home_comp'].append('coverage')
    config.add_route('coverage', pattern='/coverage')
    config.add_view(views.coverage, route_name='coverage', renderer='coverage.mako')

    #config.registry.settings['home_comp'].append('stability')
    #config.add_route('stability', pattern='/stability')
    #config.add_view(views.stability, route_name='stability', renderer='stability.mako')

    #config.registry.settings['home_comp'].append('dependencies')
    #config.add_route('dependencies', pattern='/dependencies')
    #config.add_view(views.dependencies, route_name='dependencies', renderer='dependencies.mako')
    
    config.register_resource('dependency', Dependency, IDependency, with_index=True)
    config.register_resource('transition', Transition, ITransition, with_index=True)
    config.register_resource('stability', Stability, IStability, with_index=True)
    config.register_resource('deepfamily', DeepFamily, IDeepFamily, with_index=True)
    config.register_resource('support', Support, ISupport, with_index=True)

    config.registry.registerUtility(MyMapMarker(), IMapMarker)

    config.registry.registerUtility(link_attrs, ILinkAttrs)
    config.register_datatable('familys', Families)
    return config.make_wsgi_app()
