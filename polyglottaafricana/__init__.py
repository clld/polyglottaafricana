from pyramid.config import Configurator

from clld_glottologfamily_plugin import util

from clld.interfaces import IMapMarker, IValueSet, IValue, ILinkAttrs
from clldutils.svg import pie, icon, data_url

# we must make sure custom models are known at database initialization!
from polyglottaafricana import models


_ = lambda s: s
_('Parameters')
_('Parameter')


class LanguageByFamilyMapMarker(util.LanguageByFamilyMapMarker):
    def __call__(self, ctx, req):
    
        if IValueSet.providedBy(ctx):
            if ctx.language.family:
                return data_url(icon(ctx.language.family.jsondata['icon']))
            return data_url(icon(req.registry.settings.get('clld.isolates_icon', util.ISOLATES_ICON)))
    
        return super(LanguageByFamilyMapMarker, self).__call__(ctx, req)


def link_attrs(req, obj, **kw):
    if IValue.providedBy(obj):
        # we are about to link to a value details page: redirect to valueset page!
        kw['href'] = req.route_url('valueset', id=obj.valueset.id, **kw.pop('url_kw', {}))
    return kw


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('clld.web.app')

    config.include('clldmpg')

    config.registry.registerUtility(link_attrs, ILinkAttrs)
    config.registry.registerUtility(LanguageByFamilyMapMarker(), IMapMarker)

    return config.make_wsgi_app()
