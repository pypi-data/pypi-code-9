# -*- coding: utf-8 -*-
from __future__ import absolute_import

import io

import requests
import arrow
import uuid
import six
import operator
import re
import logging

from suds.servicedefinition import WebFault

try:
    from functools import lru_cache
except ImportError:
    from functools32 import lru_cache

from .portal import Portal, TLSError
from .exceptions import BaseError

logger = logging.getLogger(__name__)

"""VidyoReplay conference recording management per user"""

__all__ = ['Replay', 'NotFoundError', 'Error']


def _closure_from_filterset(filterset):
    """
    We have to use an extra layer of indirection to create a true closure
    for the lambda generator expression, used in ``Replay.filter`` otherwise the
    lambda references the last value of ``y`` in the generator expression.
    Shame you can't do assignment in lambdas...
    """
    func, op, val = filterset
    logger.debug("closing over %r(%r, %r)", func, op, val)
    return lambda record: func(op, record, val)


def _alt_map(x, funcs):
    """
    A map function that applies an iterable of functions to a single
    datum, returning the results of each call over the data rather than the usual
    otherway around
    """
    return map(lambda f: f(x), funcs)


class Error(BaseError):
    pass


class NotFoundError(LookupError, Error):
    pass


class _ReplayFilters(object):
    """
    filter functions implementing the ``Replay.filter(**filters)``.
    each function takes a predicate function, a Record from the Replay, and a
    value for the predicate function to compare.
    """
    # This would be a simple dictionary of lambdas, but Python's lambdas
    # don't make that easy.
    @staticmethod
    def _normalize_time_val(arg):
        """
        Convert the value ``arg`` to an offset aware datetime or a list of such
        objects
        """
        # special case for bool being converted silently to int
        # https://github.com/crsmithdev/arrow/issues/238
        if isinstance(arg, bool) or arg is None:
            raise TypeError("(bool, None) -> datetime conversion semantics are invalid")
        try:
            if isinstance(arg, (list, tuple)):
                a = []
                for x in arg:
                    if hasattr(arg, 'utcoffset'):
                        if arg.utcoffset() is None:
                            raise TypeError("can't compare offset-naive and offset-aware datetimes")
                    a.append(arrow.get(x) if x is not None else None)
                arg = a
            else:
                try:
                    if arg.utcoffset() is None:
                        raise ValueError("can't compare offset naive timezone")
                except AttributeError:
                    pass
                arg = arrow.get(arg)
        except arrow.parser.ParserError:
            raise ValueError("Cannot parse %r into date" % arg)
        return arg

    @staticmethod
    def start(operator, record, arg):
        logger.debug("comparing start times %r(%r, %r)", operator, record.dateCreated, arg)
        start = arrow.get(record.dateCreated)

        logger.debug("comparing start times %r(%r, %r)", operator, start, arg)
        return operator(start, _ReplayFilters._normalize_time_val(arg))

    @staticmethod
    def end(operator, record, arg):
        logger.debug("comparing end times %r(%r, %r)", operator, record.endTime, arg)

        # We need a special-case for NULL endTime for conferences in progress
        if record.endTime is None:
            return operator(None, arg)

        end = arrow.get(record.endTime)
        if arg is None:
            return operator(end, None)
        return operator(end, _ReplayFilters._normalize_time_val(arg))

    @staticmethod
    def id(operator, record, arg):
        logger.debug("comparing ids %r(%r, %r)", operator, record.id, arg)
        return operator(int(record.id), arg)

    @staticmethod
    def uuid(operator, record, arg):
        logger.debug("comparing uuid %r(%r, %r)", operator, record.guid, arg)
        if isinstance(arg, uuid.UUID):
            id = arg
        elif isinstance(arg, six.string_types + (six.binary_type,)):
            id = uuid.UUID(arg)
        elif isinstance(arg, (list, tuple)):
            id = [x if isinstance(x, uuid.UUID) else uuid.UUID(x) for x in arg]
        else:
            raise TypeError("%s not comparable to UUID")
        return operator(uuid.UUID(record.guid), id)

    @staticmethod
    def room(operator, record, arg):
        logger.debug("comparing rooms %r(%r, %r)", operator, record.roomName, arg)
        return operator(record.roomName, arg)

    @staticmethod
    def tenant(operator, record, arg):
        logger.debug("comparing tenants %r(%r, %r)", operator, record.tenantName, arg)
        return operator(record.tenantName, arg)

    @staticmethod
    def webcast(operator, record, arg):
        logger.debug("comparing webcast %r(%r, %r)", operator, record.webcast, arg)
        return operator(record.webcast, arg)

    @staticmethod
    def display_name(operator, record, arg):
        logger.debug("comparing display_name %r(%r, %r)", operator, record.userFullName, arg)
        return operator(record.userFullName, arg)

    @staticmethod
    def duration(operator, record, arg):
        logger.debug(
            "comparing durations %r(%r - %r, %r)",
            operator, record.endTime, record.dateCreated, arg
        )
        start = arrow.get(record.dateCreated)
        try:
            if record.endTime is None:
                end = arrow.utcnow()
            else:
                end = arrow.get(record.endTime)
            if isinstance(arg, (int, float, six.string_types)):
                arg = arrow.get(arg)
            if isinstance(arg, (list, tuple)):
                arg = [arrow.get(x).datetime for x in arg]
        except arrow.parser.ParserError:
            raise ValueError("can't parse %r into duration" % arg)
        return operator(end - start, arg)

    @staticmethod
    def file_size(operator, record, arg):
        logger.debug("comparing file size %r(%r, %r)", operator, record.fileSize, arg)
        # Someone at Vidyo: What's the best way to represent an integer? Why a string of course!
        size = int(record.fileSize)
        return operator(size, arg)

    @staticmethod
    def resolution(operator, record, arg):
        logger.debug("comparing resolution %r(%r, %r)", operator, record.resolution, arg)
        return operator(record.resolution, arg)

    @staticmethod
    def framerate(operator, record, arg):
        logger.debug("comparing framerate %r(%r, %r)", operator, record.framerate, arg)
        return operator(record.framerate, arg)


class _RecordingIO(io.BytesIO):
    """
    File-like object that wraps a raw HTTP request, for the given ``recording_url``
    that must be available to the authenticated ``replay``. Allows incremental
    streaming of the recording without requiring a blocking read of the whole
    HTTP request body which may be substantial. Can be passed to functions that
    expect a standard ``file`` object.
    No HTTP requests are made until the ``read`` or ``tell`` methods are called on
    an instance of ``_RecordingIO``, so it is safe to instantiate this as part of
    a list comprehension:
        >>> my_replay = Replay(host, user=user, password=password)
        >>> # No HTTP requests made:
        >>> my_recordings = [_RecordingIO(url) for url in my_replay]
    """
    def __init__(self, replay, recording_url):
        self._replay = replay
        self._url = recording_url
        self._fp = None # Explicitly don't setup the file pointer, to defer HTTP request

    @lru_cache()
    def _recording_fp(self):
        r = self._replay.session.get(
            self._url,
            auth=(self._replay.username, self._replay.password),
            stream=True
        )
        r.raise_for_status()
        return r.raw

    def read(self, size=-1):
        if self.closed:
            raise ValueError("I/O on closed file")
        return self._recording_fp().read(size)

    def close(self):
        self._recording_fp().close()
        return super(_RecordingIO, self).close()

    def tell(self):
        if self.closed:
            raise ValueError("I/O on closed file")
        return self._recording_fp().tell()


@six.python_2_unicode_compatible
class Replay(object):
    """
    Access a user's library of conference recordings, with helpers for filtering
    and downloading the recordings.
    """
    def __init__(self, host, user=None, password=None, **kwargs):
        self.username = user
        self.password = password
        self.ssl = kwargs.get('ssl', True)

        self.replay = Portal(
            host,
            user=self.username,
            password=self.password,
            api_type='replay',
            ssl=self.ssl
        )

        self.service = self.replay.service
        self.session = requests.Session()

    @property
    @lru_cache()
    def all_records(self):
        """
        This is an in-memory view of the recordings on the replay; a memoized
        iterator to avoid the time-cost of fetching a fresh response. This is
        ususally good enough, but has implications for the lifetime of the object,
        so it is expected to be instantiated only for short-lived objects.
        """
        return list(self._uncached_iter())

    def _uncached_iter(self):
        """
        An iterator over all recordings on the replay. Since the replay
        has no real API to limit the lookup criteria we just dive in and fetch
        this all.
        Although this will not scale, it is expected to work out fine in
        practice, because one human can't record *that* many videos...right?

        **Warning** This method hits the network on every call.
        """
        try:
            index = 0
            while True:
                """
                Iterate over all recordings. The replay will return a maximum of 200
                records at a time. This nested loop stucture covers that fact up.
                """
                result = self.service.RecordsSearch(start=index)
                try:
                    records = result.records
                except AttributeError:
                    # 'records' isn't on the response when the set is empty
                    raise StopIteration
                for record in records:
                    # XXX the portal seems to make case-insensitive usernames, though
                    # this assumption will probably cause issues as it's not
                    # documented
                    if record.userName.lower() == self.replay.user.lower():
                        yield record
                index += len(records)
        except WebFault as e:
            raise Error(e)

    @lru_cache()
    def _identifier_to_record(self, record):
        """Get a record by its guid, or integer index"""
        logger.debug("converting %r to replay record")
        try:
            try:
                # If it's not a UUID we'll get a ValueError
                record = uuid.UUID(record)
                return list(filter(lambda x: uuid.UUID(x.guid) == record, self.all_records))[0]
            except (ValueError, AttributeError):
                record = int(record)
                return list(filter(lambda x: int(x.id) == int(record), self.all_records))[0]
        except (IndexError, ValueError):
            raise NotFoundError("recording %r was not found" % record)

    def delete(self, record):
        """
        Delete the given `record` from the 'replay permanently.
        `record` should be a uuid or an integer primary key.
        """
        record = self._identifier_to_record(record)
        logger.info("deleting recording: %r", record.guid)
        self.replay.service.DeleteRecord(record.id)

    def open(self, record):
        """
        Get a file-like object of the recording identified by `record`
        (an integer or uuid) returns a binary readonly file-like object.
        """
        record = self._identifier_to_record(record)
        if self.ssl:
            if not six.moves.urllib_parse.urlparse(record.fileLink).scheme == 'https':
                raise TLSError("unable to get file over https")

        return _RecordingIO(self, record.fileLink)

    def recording_content_iter(self, record, chunksize=4096):
        """Get a generator function that fetches blocks of the given record
        to allow incremental reading of the given recording.
        """
        url = self._identifier_to_record(record).fileLink
        if self.ssl:
            assert six.moves.urllib_parse.urlparse(url).scheme == 'https'

        response = self.session.get(
            url,
            auth=(self.replay.user, self.replay.password),
            stream=True
        )
        response.raise_for_status()
        return response.iter_content(chunksize)

    def recording_content(self, record):
        """
        Downloads a complete recording from the replay.
        Note that the complete video file is retrieved in-memory so retrieving
        long conferences this way may cause memory exhaustion. If this is a
        concern use `open()` instead.
        """
        return b''.join(self.recording_content_iter(record))

    def filter(self, *args, **kwargs):
        """
        Instantiate a list of recordings from the 'replay that match the search
        terms given as `kwargs`.
        The replay uses an unusual, inflexible search mechanism, so this method
        marshals a sane filter set into a bizarro one.

        The queries are like a very simplified version of the Django QuerySet API.
        filtering against the following fields are supported:

            start=x :type(x) == datetime.datetime; match recordings commencing at `x`
            end=x :type(x) == datetime.datetime; match recordings ending at `x`
            uuid=x: type(x) == uuid.UUID; match recordings with the given UUID.
            id=x: type(x) == int; get the given integer id.
            room=x: type(x) == int; filter recordings of conferences in `room` (an entityID)
            tenant=x: type(x) == str; match recordinds made by the given tenant.
            displayname: type(x) == str; match the given username.
            resolution: type(x) == str; match the name of the resolution: 'CIF', 'HD' etc

        All fields above support less-than greater-than, in, not in, equality, inequality
        in any combination.

        e.g:
        >>> recordings = Replay('example.com', 'user', 'pass').filter(
            duration__lt=timedelta(hours=1),
            resolution__ni=['HD', 'QHD'],
            filesize__gte=1e9,
            start_time__gte=now() - timedelta(days=7),
            start_time__lte=now() - timedelta(days=2),
            tenant='mytenant'
        )

        will filter for all standard-definition recordings made on 'mytenant'
        under a gigabyte in size, less than an hour in length made during a
        time-window five days long beginning last week.

        A single optional positional argument controls caching behaviour.

        e.g.
        >>> recordings = Replay('example.com', 'user', 'pass').filter(
                False, filesize__gte=1e9
        )

        ...results in the cache being disabled and will return fresh results for
        all recordings greater than a gigabyte in size.

        Bear in mind that the implementation does not handle short-circuit logic
        in the given arguments (this is impossible due the indeterminate order
        of keyword args - see PEP0468), which may adversely affect performance
        with a large number of filter predicates.
        """
        # The replay can only search with queries against the username string
        # rather than a matching set of types and corresponding predicate
        # variables.  This is totally broken behaviour so we get around this by
        # downloading a list of all recordings, and then filtering against the given
        # data client-side.

        cache = True
        if args:
            cache = args[0]
        all_records = self.all_records if cache else list(self._uncached_iter())

        # At the moment we support the following search constraints
        filters = {
            'start': _ReplayFilters.start,
            'end': _ReplayFilters.end,
            'uuid': _ReplayFilters.uuid,
            'id': _ReplayFilters.id,
            'room': _ReplayFilters.room,
            'tenant': _ReplayFilters.tenant,
            'display_name': _ReplayFilters.display_name,
            'duration': _ReplayFilters.duration,
            'resolution': _ReplayFilters.resolution,
            'file_size': _ReplayFilters.file_size,
            'framerate': _ReplayFilters.framerate,
        }
        operators = {
            'lt': operator.lt, 'gt': operator.gt, 'ne': operator.ne,
            'in': lambda x, y: operator.contains(y, x),
            'ni': lambda x, y: operator.not_(operator.contains(y, x)),
            'gte': operator.ge, 'lte': operator.le
        }

        # Encapsulate the lookup static method and the appropriate
        # value by matching kwargs with the correct function. Similar to zip()
        filters_with_args = []
        matcher = re.compile('(%s)(%s)?$' % (
            '|'.join(filters),
            '|'.join('__' + op for op in operators)
        ))
        for keyword in kwargs:
            match = matcher.match(keyword)
            if not match:
                raise ValueError("unsupported lookup %s" % keyword)
            field, op = match.groups()
            # As with django models, no double undescore suffix means the equality operator
            if op is None:
                op = operator.eq
            else:
                op = operators[op.lstrip('__')]
            logger.debug(
                "adding filter %r with operator %r and value %r",
                filters[field], op, kwargs[keyword]
            )
            filters_with_args.append((filters[field], op, kwargs[keyword]))

        # This is our bunch of funcs which are dynamically generated so as to
        # emulate the ability for map() to pass multiple arguments to its callee
        # we have to use the extra layer if indirection via the
        # _closure_from_filterset() function because python references the variable
        # rather than captures the value of y at lambda

        # This must be a list, not a generator as we use it multiple times
        filter_funcs = [_closure_from_filterset(filterset) for filterset in filters_with_args]
        logger.debug("filter_funcs: %r", filter_funcs)

        # Now apply all the generated filters to each record in turn.
        # We're only interested in records that give True for all in {filter_funcs}
        return list(six.moves.filter(
            lambda record: all(_alt_map(record, filter_funcs)), all_records)
        )

    def __iter__(self):
        return (x for x in self.all_records)

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        return self.__close__(*args, **kwargs)

    def __close__(self, *args, **kwargs):
        self.session.close()

    def __len__(self):
        """
        len() will return the number of recordings found in the lookup.
        """
        return len(self.all_records)

    def __str__(self):
        return "%s(%r@%r)" % (
            self.__class__.__name__,
            self.replay.user,
            self.replay.url.geturl(),
        )
