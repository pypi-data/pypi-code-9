

class QueryError(Exception):
    "Exception to handle when dealing with queries"
    pass


class DatabaseBackendBase(object):

    def start_bulk(self):
        self.bulk_query = []
        return self.bulk_query

    def commit_bulk_create(self):
        raise NotImplementedError

    def clean_token(self, token):
        return token.split('.')[1]

    def add_filter(self, key, value):
        raise NotImplemented('need to implement add filter for this class')


class QuerySet(object):
    """
        allows database query results to be
        lazily instantiated
    """

    default_query = None

    def __init__(self, query=None, model=None, db=None, offset=0, apply_data=None):
        self._result_cache = None
        self.query = query or self.default_query
        self.model = model
        self.db = db
        self.applied_data=apply_data

        self.offset = offset

    @property
    def results(self):
        """
            only hit the database if we don't have
            a result cache.  otherwise return that instead
        """
        if not self._result_cache:
            try:
                self._result_cache = self.model.instantiate_list(
                    self.query,
                    read_from_db=True,
                    offset=self.offset,
                    from_json=False,
                    applied_data=self.applied_data
                )
            except Exception, e:
                raise
                print 'r:',r
        return self._result_cache

    def __iter__(self):
        return iter(self.results)

    def __getitem__(self, index):
        if self.results:
            return self.results[index]
        return None

    def __len__(self):
        if self.results:
            return len(self.results)
        return 0

    def count(self):
        return len(self.results)

    def as_list(self):
        return [o.as_dict() for o in self.results]
