import six

try:
    # We used to require mysql-python, but it's broken for non-CPython or CPython > 3
    # This allows us to fail down to MySQLdb gracefully.
    import pymysql
    pymysql.install_as_MySQLdb()
except ImportError:
    pass

import MySQLdb
import MySQLdb.cursors
import arrow

from . import Error

__all__ = ['CDRInfo']


class CDRError(Error):
    pass


class TransportError(CDRError):
    pass


class NotFoundError(CDRError):
    pass


class _Credentials(object):
    """default wrapper for a bunch of connection information."""
    def __init__(self, **kwargs):
        self.user = kwargs.get('sqluser', 'cdraccess') or 'cdraccess'
        self.port = kwargs.get('port', 3306) or 3306
        self.host = kwargs.get('host', 'localhost') or 'localhost'
        self.password = kwargs.get('password', None)
        self.timeout = kwargs.get('timeout', 5) or 5


class _MySQLCDRWrapper(object):
    """Vidyo Schema Wrapper around MySQLdb to provide
    Call Detail records for a given VidyoPortal username
    """

    def __init__(self, membername, mysql_credentials, vidyo_schema=2, **kwargs):
        assert isinstance(membername, six.string_types)
        assert vidyo_schema in (1, 2)
        self.membername = membername
        self.db_name = kwargs.get('dbname', vidyo_schema == 2 and 'portal2' or 'portal')
        self.conference_table = vidyo_schema == 2 and 'ConferenceCall2' or 'ConferenceCall'
        try:
            self.db = MySQLdb.connect(
                user=mysql_credentials.user,
                host=mysql_credentials.host,
                db=self.db_name,
                port=mysql_credentials.port,
                connect_timeout=mysql_credentials.timeout,
                passwd=mysql_credentials.password,
            )
        except Exception as e:
            raise TransportError(e)

        self.cursor = self._new_cursor()
        self.cursor.execute("""SELECT @@global.system_time_zone;""")
        self.sql_tz = self.cursor.fetchone()['@@global.system_time_zone']

    def _new_cursor(self):
        curs = MySQLdb.cursors.DictCursor(self.db)
        # This probably won't help with error 2014, but it may be useful
        curs.connection.autocommit(True)
        return curs

    def _mysql_to_tz_aware(self, date):
        """
        MySQL's timezone handling is retarded.
        This goes some way to fixing that.
        """
        return arrow.get(date, self.sql_tz)

    def _mysql_as_utc(self, date):
        """
        Take a date returned by MySQL and format it as a timezone aware
        UTC date (arrow)
        """
        if isinstance(date, arrow.Arrow):
            return date.to('UTC')
        return self._mysql_to_tz_aware(date).to('UTC')

    def _calls_as_utc(self, calls):
        """Given a call or list of calls, convert all date members
        to timezone aware UTC representations.
        """
        if not hasattr(calls, '__iter__'):
            calls = (calls,)
        for call in calls:
            call['JoinTime'] = self._mysql_as_utc(call['JoinTime'])
            call['LeaveTime'] = self._mysql_as_utc(call['LeaveTime'])
        return calls

    def in_confcall(self):
        """
        Check whether the given user is currently in a conference call.
        """
        count = self.cursor.execute(
            """SELECT CallerID, CallState from """ + self.conference_table +
            """ WHERE (CallerID, CallState) = (%s, 'IN PROGRESS')""",
            (self.membername,)
        )
        if count:
            return True
        return False

    def live_confcall_id(self):
        """
        Retrieve Vidyo's UniqueCallID for the user's live call (if any).
        """
        count = self.cursor.execute(
            """SELECT UniqueCallID from """ + self.conference_table +
            """ WHERE (CallerID, CallState) = (%s, 'IN PROGRESS')""",
            (self.membername,)
        )
        if not count:
            return None
        assert count == 1
        return self.cursor.fetchone()['UniqueCallID']

    def usernames_in_room(self, callid=None):
        """
        Given a UniqueCallID, gets a list of the users in that room.
        Otherwise, checks for a live call, and gives the users in that calls
        """
        if callid is None:
            callid = self.live_confcall_id()
            if callid is None:
                return None
        count = self.cursor.execute(
            """SELECT CallerID FROM """ + self.conference_table +
            """ WHERE UniqueCallID = %s""", (callid,),
        )
        if not count:
            raise NotFoundError("Given UniqueCallID doesn't exist:%s" % callid)
        names = [name.values()[0] for name in self.cursor.fetchall()]
        return names

    def total_confcalls(self):
        """Get the number of conferences calls made by this user
        (including those in progress)"""
        self.cursor.execute(
            """SELECT COUNT(*) from ConferenceCall2 WHERE CallerID = %s""",
            (self.membername,)
        )
        return self.cursor.fetchone()['COUNT(*)']

    def all_confcalls(self):
        """Get everything.  All datetime members will be UTC"""
        try:
            total_calls = self.cursor.execute(
                """SELECT * FROM """ + self.conference_table +
                """ WHERE CallerID = %s""", (self.membername,))
            if total_calls:
                return self._calls_as_utc(self.cursor.fetchall())
            else:
                return None
        except Exception as e:
            raise TransportError("couldn't get db cursor %s" % e.message)

    def all_confcalls_iter(self):
        """
        Creates a generator that yields all the conference calls
        Kind of pointless at the moment because MySQLdb fetches all
        results in memory regardless of the use of MySQLdb.cursors.SSDictCursor.

        Once the behaviour of iterable responses has been sorted, using this will make sense.
        """
        cursor = self._new_cursor()
        try:
            total_calls = cursor.execute(
                """SELECT * FROM """ + self.conference_table +
                """ WHERE CallerID = %s""", (self.membername,))
        except Exception as e:
            raise TransportError("couldn't get db cursor %s" % e.message)

        def iterfn():
            for x in six.moves.range(total_calls):
                call = cursor.fetchone()
                call['JoinTime'] = self._mysql_as_utc(call['JoinTime'])
                call['LeaveTime'] = self._mysql_as_utc(call['LeaveTime'])
                yield call
            cursor.close()

        return iterfn

    def last_n_confcalls(self, n):
        """
        Get the most recently completed calls, ordered by time of completion.
        Does not include calls in progress.
        """
        total_calls = self.cursor.execute(
            """SELECT * FROM """ + self.conference_table +
            """ WHERE CallerID = %s ORDER BY LeaveTime DESC LIMIT %s """,
            (self.membername, int(n)),
        )
        if not total_calls:
            return tuple()
        return self._calls_as_utc(self.cursor.fetchall())

    def first_n_calls(self, n):
        """
        Get the {n} most recently completed calls, ordered by time of completion.
        Does not include calls in progress.
        """
        total_calls = self.cursor.execute(
            """SELECT * FROM """ + self.conference_table +
            """ WHERE CallerID = %s ORDER BY LeaveTime ASC LIMIT %s """,
            (self.membername, int(n)),
        )
        if not total_calls:
            return tuple()
        return self._calls_as_utc(self.cursor.fetchall())

    def between(self, start=None, end=None):
        """
        Get all conference calls between the two given dates.
        {start} and {end} are expected to be tz-aware.
        """
        all_calls = self.all_confcalls()
        start = start or arrow.utcnow() - arrow.util.timedelta.max
        end = end or arrow.utcnow()
        return [call for call in all_calls if call['JoinTime'] > start and call['LeaveTime'] < end]

    def after(self, date):
        try:
            total_calls = self.cursor.execute(
                """SELECT * FROM """ + self.conference_table +
                """ WHERE JoinTime > %s""", (self.membername,))
            if total_calls:
                return self._calls_as_utc(self.cursor.fetchall())
            else:
                return None
        except Exception as e:
            raise TransportError("couldn't get db cursor %s" % e.message)

    def before(self, data):
        raise NotImplementedError()

    def close(self, *args):
        """clean up automatically on object destruction. Use with ``contextlib.closing``"""
        self.db.close()


class CDRInfo(_MySQLCDRWrapper):
    """
    An interface to conference records available in the Portal's MySQL database.

    Takes the following parameters.
    `user` the Vidyo username to query (Required)
    `host` the FQDN of the VidyoPortal. (Required)
    `password` the mysql password. (Required)
    `sqluser` the username for the mysql instance (default='cdraccess')
    `port` where is mysql listening (default=3306)
    `timeout` how long in seconds to try to connect before failure (default=5)
    `vidyo_schema` The particular version of the Portal.
        This affects which databases and tables are used.
        Version 2 has more information available.
        Vidyo changed this with the release of Portal version 2 (default=2)

    Instances of this object should be used in a `closing` context manager, or
    connections to MySQL may not be properly terminated, and lead to CHAOS:

    >>> with contextlib.closing(CDRInfo()) as records:
        print("I am active?: %r" % records.in_confcall())
    """
    def __init__(self, **kwargs):
        cred_args = ('sqluser', 'password', 'host', 'port', 'timeout', 'sslcert')
        creds = {key: val for key, val in kwargs.items() if key in cred_args}
        [kwargs.pop(key, None) for key in cred_args]
        super(self.__class__, self).__init__(
            kwargs.get('user'),
            _Credentials(**creds),
            kwargs.get('vidyo_schema', 2),
            **kwargs
        )
