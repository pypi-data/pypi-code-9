from __future__ import absolute_import

from confpages.loaders import Page, Loader


class DummyLoader(Loader):
    """The dummy page loader."""

    def get_page(self, name, only_api_url=False):
        """Retrieve the page object."""
        page = Page(name, api_url='http://localhost/dummy-api')
        if not only_api_url:
            page.title = name.capitalize()
            page.content = 'This is the {} page'.format(page.title)
        return page


class DummyAPILoader(Loader):
    """The dummy page loader only for returning api_url."""

    def get_page(self, name, only_api_url=False):
        """Retrieve the page object."""
        page = Page(name, api_url='http://localhost/dummy-api')
        return page
