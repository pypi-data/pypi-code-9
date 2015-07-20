import bloop.column
import bloop.condition
import bloop.index
import operator

SELECT_MODES = {
    "all": "ALL_ATTRIBUTES",
    "projected": "ALL_PROJECTED_ATTRIBUTES",
    "specific": "SPECIFIC_ATTRIBUTES",
    "count": "COUNT"
}


def consume(iter):
    for _ in iter:
        pass


def validate_key_condition(condition):
    if isinstance(condition, (bloop.condition.BeginsWith,
                              bloop.condition.Between)):
        return True
    elif isinstance(condition, bloop.condition.Comparison):
        # Valid comparators are EG | LE | LT | GE | GT -- not NE
        if condition.comparator is not operator.ne:
            return True
    raise ValueError("Invalid KeyCondition {}".format(condition))


def validate_prefetch(value):
    invalid = ValueError("prefetch must be `all` or a non-negative int")
    if value != "all":
        try:
            value = int(value)
        except ValueError:
            raise invalid
        else:
            if value < 0:
                raise invalid
    return value


def validate_select_mode(select):
    invalid = ValueError("Must specify 'all', 'projected', 'count', or"
                         " a list of column objects to select")
    if isinstance(select, str):
        select = select.lower()
        if select not in ["all", "projected", "count"]:
            raise invalid
    else:
        try:
            select = list(select)
        except TypeError:
            raise invalid
        if not select:
            raise invalid
        for column in select:
            if not isinstance(column, bloop.column.Column):
                raise invalid
    return select


class Filter(object):
    '''
    Base class for Scan and Query.
    '''
    # Scan -> 'scan', Query -> 'query'
    filter_type = None

    def __init__(self, engine, *, model=None, index=None):
        self.engine = engine
        self.model = model
        self.index = index

        self._key_condition = None
        self._filter_condition = None
        if self.index:
            self._select = "projected"
        else:
            self._select = "all"
        self._forward = True
        self._consistent = False

        self._select_columns = []

    def _copy(self):
        cls = self.__class__
        other = cls(engine=self.engine, model=self.model, index=self.index)

        for attr in ["_filter_condition", "_key_condition",
                     "_select", "_forward", "_consistent"]:
            setattr(other, attr, getattr(self, attr))

        other._select_columns = list(self._select_columns)
        other._key_condition = self._key_condition
        return other

    def _expected(self):
        '''
        Return a list of Columns that are expected for the current options.
        '''
        if self._select == 'all':
            return self.model.Meta.columns
        elif self._select == 'projected':
            return self.index.projection_attributes
        # specific
        else:
            # If more are requested than a LSI supports, all will be loaded.
            # In all other cases, just the selected columns will be.
            if isinstance(self.index, bloop.index.LocalSecondaryIndex):
                selected = set(self._select_columns)
                available = self.index.projection_attributes
                if not selected.issubset(available):
                    return self.model.Meta.columns
            return self._select_columns

    def _generate_request(self, renderer):
        request = {
            'TableName': self.model.Meta.table_name,
            'Select': SELECT_MODES[self._select]
        }
        if self.index:
            request['IndexName'] = self.index.dynamo_name
        if self._filter_condition:
            renderer.render(self._filter_condition, mode="filter")
        if self._select == "specific":
            renderer.projection(self._select_columns)
        request.update(renderer.rendered)
        return request

    def all(self, prefetch=None):
        '''
        Creates the FilterResult that will lazy load the results of the
        scan/query.

        Usage:
            base_query = engine.query(Model).key(id='foo')
            query = base_query.consistent.ascending

            # Iterate results directly, discarding query metadata
            for result in query:
                ...

            # Save reference to FilterResult instance
            results = query.all()
            for result in results:
                ...
            print(results.count, results.scanned_count)
        '''
        if prefetch is None:
            prefetch = self.engine.config["prefetch"]
        # dynamo.client.query or dynamo.client.scan
        call = getattr(self.engine.client, self.filter_type)
        renderer = bloop.condition.ConditionRenderer(self.engine)
        request = self._generate_request(renderer)

        expected = self._expected()
        return FilterResult(prefetch, call, request, self.engine,
                            self.model, expected)

    @property
    def ascending(self):
        other = self._copy()
        other._forward = True
        return other

    @property
    def consistent(self):
        if isinstance(self.index, bloop.index.GlobalSecondaryIndex):
            raise ValueError(
                "Cannot use ConsistentRead with a GlobalSecondaryIndex")
        other = self._copy()
        other._consistent = True
        return other

    def count(self):
        other = self._copy()
        other._select = "count"
        other._select_columns.clear()
        # Force fetch all
        result = other.all(prefetch="all")
        return {
            "count": result.count,
            "scanned_count": result.scanned_count
        }

    @property
    def descending(self):
        other = self._copy()
        other._forward = False
        return other

    def filter(self, condition):
        other = self._copy()
        # AND multiple filters
        if other._filter_condition:
            condition &= other._filter_condition
        other._filter_condition = condition
        return other

    def first(self):
        ''' Returns the first result that matches the filter. '''
        result = self.all(prefetch=0)
        return result.first

    def key(self, condition):
        # AND multiple conditions
        if self._key_condition:
            condition &= self._key_condition

        obj = self.index or self.model.Meta
        hash_column = obj.hash_key
        range_column = obj.range_key

        max_conditions = 1 + bool(range_column)

        if not condition:
            raise ValueError("At least one key condition (hash) is required")

        # AND is allowed so long as the index we're using allows hash + range
        if isinstance(condition, bloop.condition.And):
            if max_conditions < len(condition):
                msg = ("Model or Index only allows {} condition(s) but"
                       " an AND of {} condition(s) was supplied.").format(
                           max_conditions, len(condition))
                raise ValueError(msg)
            # KeyConditions can only use the following:
            # EQ | LE | LT | GE | GT | BEGINS_WITH | BETWEEN
            for subcond in condition.conditions:
                validate_key_condition(subcond)

            columns = set(subcond.column for subcond in condition.conditions)
            # Duplicate column in AND
            if len(columns) < len(condition):
                raise ValueError("Cannot use a hash/range column more"
                                 " than once when specifying KeyConditions")

            if hash_column not in columns:
                raise ValueError("Must specify a hash key")

            # At this point we've got the same number of columns and
            # conditions, and that's less than or equal to the number of
            # allowed conditions for this model/index.

        # Simply validate all other conditions
        else:
            validate_key_condition(condition)
            if condition.column is not hash_column:
                raise ValueError("Must specify a hash key")

        other = self._copy()
        other._key_condition = condition
        return other

    def select(self, columns):
        '''
        columns must be 'all', 'projected', or a list of `bloop.Column` objects
        '''
        select = validate_select_mode(columns)
        is_gsi = isinstance(self.index, bloop.index.GlobalSecondaryIndex)
        is_lsi = isinstance(self.index, bloop.index.LocalSecondaryIndex)
        strict = self.engine.config["strict"]
        requires_exact = (is_gsi or (is_lsi and strict))

        if select == "count":
            other = self._copy()
            other._select = select
            other._select_columns.clear()
            return other

        elif select == 'projected':
            if not self.index:
                raise ValueError("Cannot select 'projected' attributes"
                                 " without an index")
            other = self._copy()
            other._select = select
            other._select_columns.clear()
            return other

        elif select == 'all':
            if requires_exact and self.index.projection != "ALL":
                raise ValueError("Cannot select 'all' attributes from a GSI"
                                 " (or an LSI in strict mode) unless the"
                                 " index's projection is 'ALL'")
            other = self._copy()
            other._select = select
            other._select_columns.clear()
            return other

        # select is a list of model names, use 'specific'
        else:
            # Combine before validation, since the total set may no longer
            # be valid for the index.
            other = self._copy()
            other._select = 'specific'
            other._select_columns.extend(select)

            if requires_exact and self.index.projection != "ALL":
                projected = self.index.projection_attributes
                missing_attrs = set(other._select_columns) - projected

                if missing_attrs:
                    msg = ("Index projection is missing the following expected"
                           " attributes, and is either a GSI or an LSI and"
                           " strict mode is enabled: {}").format(
                        [attr.model_name for attr in missing_attrs])
                    raise ValueError(msg)
            return other

    def __iter__(self):
        return iter(self.all())


class Query(Filter):
    filter_type = "query"

    def _generate_request(self, renderer):
        request = super()._generate_request(renderer)
        request['ScanIndexForward'] = self._forward
        request['ConsistentRead'] = self._consistent

        if not self._key_condition:
            raise ValueError("Must specify at least a hash key condition")
        renderer.render(self._key_condition, mode="key")
        request.update(renderer.rendered)
        return request


class Scan(Filter):
    filter_type = "scan"


class FilterResult(object):
    '''
    Result from a scan or query.  Usually lazy loaded, iterate to execute.

    Uses engine.prefetch to control call batching
    '''
    def __init__(self, prefetch, call, request, engine, model, expected):
        self._call = call
        self._prefetch = validate_prefetch(prefetch)
        self.request = request
        self.engine = engine
        self.model = model
        self.expected = expected

        self.count = 0
        self.scanned_count = 0
        self._results = []
        self._continue = None
        self._complete = False

        # Kick off the full execution
        if prefetch == "all":
            consume(self)

    @property
    def complete(self):
        return self._complete

    @property
    def first(self):
        if self._results:
            return self._results[0]

        if not self.complete:
            step = iter(self)
            # Advance until we have some results, or we exhaust the query
            while not self._results and not self.complete:
                try:
                    next(step)
                except StopIteration:
                    # The step above exhausted the results, nothing left
                    break
        if not self._results:
            raise ValueError("No results found.")
        return self._results[0]

    @property
    def results(self):
        if not self.complete:
            raise RuntimeError("Can't access results until request exhausted")
        return self._results

    def __iter__(self):
        # Already finished, iterate existing list
        if self.complete:
            return iter(self.results)
        # Fully exhaust the filter before returning an iterator
        elif self._prefetch == "all":
            # Give self._continue a chance to be not None
            consume(self._step())
            while self._continue:
                consume(self._step())
            self._complete = True
            return iter(self.results)
        # Lazy load, prefetching as necessary
        else:
            return self.__prefetch_iter__()

    def __prefetch_iter__(self):
        '''
        Separate function because the `yield` statement would turn __iter__
        into a generator when we want to return existing iterators in some
        cases.
        '''
        while not self.complete:
            prefetch = self._prefetch

            objs = list(self._step())
            while self._continue and prefetch:
                prefetch -= 1
                # Doesn't need the same catch on StopIteration as in `first`
                # since self._continue would be set on the above _step call
                objs.extend(self._step())
            for obj in objs:
                    yield obj

            # Don't set complete until we've
            # yielded all objects from this step
            if not self._continue:
                self._complete = True

    def _step(self):
        ''' Single call, advancing ExclusiveStartKey if necessary. '''
        if self._continue:
            self.request["ExclusiveStartKey"] = self._continue
        response = self._call(self.request)
        self._continue = response.get("LastEvaluatedKey", None)

        self.count += response["Count"]
        self.scanned_count += response["ScannedCount"]

        results = response.get("Items", [])
        for result in results:
            obj = self.engine.__instance__(self.model)
            self.engine.__update__(obj, result, self.expected)
            self._results.append(obj)
            yield obj
