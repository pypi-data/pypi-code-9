from __future__ import absolute_import

from django.http import Http404

from confpages.loaders import Loader, Page


class MongoLoader(Loader):
    """MongoDB-based page loader."""

    #: The database instance
    database = None

    #: The collection name
    collection_name = None

    def __init__(self):
        if self.database is None:
            raise AttributeError('The class-level attribute `database` '
                                 'must be specified.')
        if self.collection_name is None:
            raise AttributeError('The class-level attribute `collection_name` '
                                 'must be specified.')
        self.engine = self.database[self.collection_name]

    def get_page(self, name, only_api_url=False):
        """Retrieve the page object."""
        fields = None
        if only_api_url:
            fields = {'api_url': True}

        record = self.engine.find_one({'name': name}, fields)
        if not record:
            raise Http404('No page named "{}" can be found in the MongoDB '
                          'collection {}'.format(name, self.collection_name))

        page = Page(
            name,
            record.get('title', ''),
            record.get('content', ''),
            record.get('is_static', True),
            record['api_url'],
            record.get('base_template')
        )
        return page
