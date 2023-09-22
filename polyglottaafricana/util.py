from clld.web.util import glottolog
from clld.web.util import concepticon


def language_detail_html(context=None, request=None, **kw):
    return context.render_inventory(request=request)
