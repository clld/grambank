from pyramid.config import Configurator
from sqlalchemy.orm import joinedload

from clld.interfaces import (
    IValue, IDomainElement, IMapMarker, IValueSet, ILinkAttrs, IContribution, ICtxFactoryQuery,
)
from clld.web.app import CtxFactoryQuery
from clld_glottologfamily_plugin.util import LanguageByFamilyMapMarker
from clld.db.models import common

# we must make sure custom models are known at database initialization!
from grambank import models
from grambank import views


_ = lambda s: s
_('Parameters')
_('Parameter')
_('Familys')


class GrambankMapMarker(LanguageByFamilyMapMarker):
    def get_icon(self, ctx, req):
        if IValue.providedBy(ctx):
            return ctx.domainelement.jsondata['icon']
        if IValueSet.providedBy(ctx):
            return ctx.values[0].domainelement.jsondata['icon']
        if IDomainElement.providedBy(ctx):
            return ctx.jsondata['icon']
        return LanguageByFamilyMapMarker.get_icon(self, ctx, req)


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
    
    config.registry.settings['home_comp'].append('coverage')
    config.add_route('coverage', pattern='/coverage')
    config.add_view(views.coverage, route_name='coverage', renderer='coverage.mako')

    config.registry.registerUtility(GrambankCtxFactoryQuery(), ICtxFactoryQuery)
    config.registry.registerUtility(GrambankMapMarker(), IMapMarker)
    config.registry.registerUtility(link_attrs, ILinkAttrs)
    return config.make_wsgi_app()
