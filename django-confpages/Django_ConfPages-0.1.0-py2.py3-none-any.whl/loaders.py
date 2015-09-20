from __future__ import absolute_import


class Page(object):
    """The page object."""

    def __init__(self, name, title='', content='', is_static=True,
                 api_url=None, base_template=None):
        # The page name
        self.name = name
        # The page title
        self.title = title
        # The page content
        self.content = content
        # Whether the page has any context data
        self.is_static = is_static
        # The url of the backend API
        self.api_url = api_url
        # The base template name
        self.base_template = base_template


class Loader(object):

    def get_page(self, name, only_api_url=False):
        """Retrieve the page object."""
        raise NotImplementedError(".get_page() must be overridden.")


class DefaultLoader(Loader):

    content = '''
<!DOCTYPE html>
<html>
  <head>
    <title>{title}</title>
  </head>
  <body>
    <p>This is the {title} page, which is provided by
    the default page loader <b>DefaultLoader</b>.</p>
    <p>The configurable pages here should be accessed via the
    url in the format of "{base_url}&lt;name&gt;". Now please
    try the following urls:</p>
    <ul><li><a href="{host}{index_url}">{index_url}</a></li>
    <li><a href="{host}{help_url}">{help_url}</a></li></ul>
    <p>In the real world, you should change the `CONFPAGES.
    PAGE_LOADER` setting in your Django settings file to use
    your own page loader, or to use the built-in <b>MongoLoader
    </b> (note that the <b>pymongo</b> library is required).</p>
  </body>
</html>
'''

    def get_page(self, name, only_api_url=False):
        """Retrieve the page object."""
        page = Page(name)
        if not only_api_url:
            from django.core.urlresolvers import reverse
            page.title = name.capitalize()
            page.content = self.content.format(
                title=page.title,
                base_url=reverse('confpages-index'),
                host='http://localhost:8000',
                index_url=reverse('confpages-detail', args=('index',)),
                help_url=reverse('confpages-detail', args=('help',))
            )
        return page
