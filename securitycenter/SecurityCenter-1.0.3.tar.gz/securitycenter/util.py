class PagedResult(list):
    #: key to get items to paginate from response data
    _key = 'results'

    def __init__(self, client, module, action, input, data):
        """Represent one page of a paged result.  Each page is a list of the items on that page,
        with methods to get subsequent pages.

        :param client: client that made the initial request
        :param module: module requested
        :param action: action requested
        :param input: input sent in request
        :param data: response data
        """

        super(PagedResult, self).__init__(data[self._key])
        data[self._key] = self

        self.client = client
        self.module = module
        self.action = action
        self.input = input

        self._set_page(input, data)
        self._set_total(input, data)
        self.has_more = self.page * self.page_size < self.total

    @staticmethod
    def _can_page(data):
        """Check whether the data can be paginated."""

        return 'totalRecords' in data

    def _set_page(self, input, data):
        """Override this in a subclass if the request doesn't return the expected page format.
        This method should set ``self.page_size`` and ``self.size``.

        :param input: input to request
        :param data: output from request
        """

        start = int(data['startOffset'])
        end = int(data['endOffset'])
        self.page_size = end + 1 - start if end > 0 else len(self)
        self.page = start // self.page_size + 1 if self.page_size > 0 else 1

    def _set_total(self, input, data):
        """Override this in a subclass if the request doesn't return the expected total format.
        This method should set ``self.total``..

        :param input: input to request
        :param data: output from request
        """

        self.total = int(data['totalRecords'])

    def _next_input(self):
        """Override this method if the request doesn't use the expected page format.
        This method should modify a copy of ``self.input``.

        :return: the new input dict
        """

        input = self.input.copy()
        input['startOffset'] = self.page_size * self.page
        input['endOffset'] = self.page_size * (self.page + 1) - 1
        return input

    def next_page(self):
        """Get the next page of results or``None`` if this is the last page."""

        if self.has_more:
            return self.client._request(self.module, self.action, input=self._next_input(), page_class=self.__class__)[self._key]

    def iter_pages(self):
        """Iterate over all pages, including the current one."""

        current = self

        while current is not None:
            yield current
            current = current.next_page()

    def iter_items(self):
        """Iterate over all items on all pages."""

        return (item for page in self.iter_pages() for item in page)
