from urllib.parse import urlencode

import sqlalchemy
from paginate import Page
from paginate_sqlalchemy import SqlalchemyOrmPage

INCOMPATIBLE_COLLECTION_TYPE = """
Sorry, your collection type is not supported by the paginate module. You can
provide a list, a tuple, or a SQLAlchemy ORM Query object."""


def make_page_url(path, params, page, partial=False, sort=True):
    """A helper function for URL generators.

    I assemble a URL from its parts. I assume that a link to a certain page is
    done by overriding the 'page' query parameter.

    ``path`` is the current URL path, with or without a "scheme://host" prefix.

    ``params`` is the current query parameters as a dict or dict-like object.

    ``page`` is the target page number.

    If ``partial`` is true, set query param 'partial=1'. This is to for AJAX
    calls requesting a partial page.

    If ``sort`` is true (default), the parameters will be sorted. Otherwise
    they'll be in whatever order the dict iterates them.
    """
    params = params.copy()
    params['page'] = page
    if partial:
        params['partial'] = '1'
    if sort:
        params = params.items()
        params.sort()
    qs = urlencode(params, True)
    return "%s?%s" % (path, qs)


class PageURL(object):
    """A simple page URL generator for any framework."""

    def __init__(self, path, params):
        """
        ``path`` is the current URL path, with or without a "scheme://host"
         prefix.

        ``params`` is the current URL's query parameters as a dict or dict-like
        object.
        """
        self.path = path
        self.params = params

    def __call__(self, page, partial=False):
        """Generate a URL for the specified page."""
        return make_page_url(self.path, self.params, page, partial)


class PageURLWebOb(object):
    """A page URL generator for WebOb-compatible Request objects.

    I derive new URLs based on the current URL but overriding the 'page'
    query parameter.

    I'm suitable for Pyramid, Pylons, and TurboGears, as well as any other
    framework whose Request object has 'application_url', 'path', and 'GET'
    attributes that behave the same way as ``webob.Request``'s.
    """

    def __init__(self, request, qualified=False):
        """
        ``request`` is a WebOb-compatible ``Request`` object.

        If ``qualified`` is false (default), generated URLs will have just the
        path and query string. If true, the "scheme://host" prefix will be
        included. The default is false to match traditional usage, and to avoid
        generating unuseable URLs behind reverse proxies (e.g., Apache's
        mod_proxy).
        """
        self.request = request
        self.qualified = qualified

    def __call__(self, page, partial=False):
        """Generate a URL for the specified page."""
        if self.qualified:
            path = self.request.application_url
        else:
            path = self.request.path
        return make_page_url(path, self.request.GET, page, partial)


def get_wrapper(obj, *args, **kwargs):
    if isinstance(obj, (list, tuple)):
        return Page(obj, *args, **kwargs)

    if isinstance(obj, sqlalchemy.orm.query.Query):
        return SqlalchemyOrmPage(obj, *args, **kwargs)

    required_methods = ["__iter__", "__len__", "__getitem__"]
    for m in required_methods:
        if not hasattr(obj, m):
            break
    else:
        return obj

    raise TypeError(INCOMPATIBLE_COLLECTION_TYPE)


def page(collection, request, items_per_page=10, url=None):
    if not url:
        url = PageURLWebOb(request)
    else:
        url = PageURL(url, {'page': int(request.GET.get('page', 1))})

    return get_wrapper(collection,
                       page=int(request.GET.get('page', 1)),
                       items_per_page=items_per_page,
                       url=url)
