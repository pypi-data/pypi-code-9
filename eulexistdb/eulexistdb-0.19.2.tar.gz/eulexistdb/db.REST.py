# file eulexistdb/db.py
#
#   Copyright 2010,2011 Emory University Libraries
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

"""Connect to an eXist XML database and query it.

This module provides :class:`ExistDB` and related classes for connecting to
an eXist-db_ database and executing XQuery_ queries against it.

.. _XQuery: http://www.w3.org/TR/xquery/
.. _eXist-db: http://exist.sourceforge.net/

When used with Django, :class:`~eulexistdb.db.ExistDB` can pull
configuration settings directly from Django settings.  If you create
an instance of :class:`~eulexistdb.db.ExistDB` without specifying a
server url, it will attempt to configure an eXist database based on
Django settings, using the configuration names documented below.



Projects that use this module should include the following settings in their
``settings.py``::

  #Exist DB Settings
  EXISTDB_SERVER_USER = 'user'
  EXISTDB_SERVER_PASSWORD = 'password'
  EXISTDB_SERVER_URL = "http://megaserver.example.com:8042/exist"
  EXISTDB_ROOT_COLLECTION = "/sample_collection"

.. note:

  User and password settings are optional.

To configure a timeout for most eXist connections, specify the desired
time in seconds as ``EXISTDB_TIMEOUT``; if none is specified, the
global default socket timeout will be used.

.. note::

  Any configured ``EXISTDB_TIMEOUT`` will be ignored by the
  **existdb** management command, since reindexing a large collection
  could take significantly longer than a normal timeout would allow
  for.

If you are using an eXist index configuration file, you can add another setting
to specify your configuration file::

  EXISTDB_INDEX_CONFIGFILE = "/path/to/my/exist_index.xconf"

This will allow you to use the ``existdb`` management command to
manage your index configuration file in eXist.

If you wish to specify options for fulltext queries, you can set a dictionary
of options like this::

    EXISTDB_FULLTEXT_OPTIONS = {'default-operator': 'and'}

.. note::

  Full-text query options are only available in very recent versions of eXist.


If you are writing unit tests against code that uses
:mod:`eulexistdb`, you may want to take advantage of
:class:`eulexistdb.testutil.TestCase` for loading fixture data to a
test eXist-db collection, and
:class:`eulexistdb.testutil.ExistDBTestSuiteRunner`, which has logic
to set up and switch configurations between a development and test
collections in eXist.

----

"""

from functools import wraps
import httplib
import logging
import requests
import socket
from urllib import unquote_plus, splittype
import urlparse
import warnings
import xmlrpclib

from eulxml import xmlmap
from eulexistdb import exceptions as exc

__all__ = ['ExistDB', 'QueryResult', 'EXISTDB_NAMESPACE']

logger = logging.getLogger(__name__)

EXISTDB_NAMESPACE = 'http://exist.sourceforge.net/NS/exist'

## TODO/NOTE: stick with xmlrpc for consistency/backwards compatibility
# but add rest api calls where it makes sense or where they are
# obviously better/simpler (e.g., load/delete)


def _wrap_xmlrpc_fault(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except socket.timeout as e:
            raise exc.ExistDBTimeout(e)
        except (socket.error, xmlrpclib.Fault, \
            xmlrpclib.ProtocolError, xmlrpclib.ResponseError) as e:
                raise exc.ExistDBException(e)
        # FIXME: could we catch IOerror (connection reset) and try again ?
        # occasionally getting this error (so far exclusively in unit tests)
        # error: [Errno 104] Connection reset by peer
    return wrapper


class ExistDB:
    """Connect to an eXist database, and manipulate and query it.

    Construction doesn't initiate server communication, only store
    information about where the server is, to be used in later
    communications.

    :param server_url: The XML-RPC endpoint of the server, typically
                       ``/xmlrpc`` within the server root.
    :param resultType: The class to use for returning :meth:`query` results;
                       defaults to :class:`QueryResult`
    :param encoding:   The encoding used to communicate with the server;
                       defaults to "UTF-8"
    :param verbose:    When True, print XML-RPC debugging messages to stdout
    :param timeout: Specify a timeout for xmlrpc connection
      requests.If not specified, the global default socket timeout
      value will be used.

    """

    def __init__(self, server_url=None, username=None, password=None,
                 resultType=None, encoding='UTF-8', verbose=False,
                 **kwargs):
        # FIXME: Will encoding ever be anything but UTF-8? Does this really
        #   need to be part of our public interface?

        self.resultType = resultType or QueryResult
        datetime_opt = {'use_datetime': True}

        # distinguish between timeout not set and no timeout, to allow
        # easily setting a timeout of None and have it override any
        # configured EXISTDB_TIMEOUT
        timeout = None
        if 'timeout' in kwargs:
            timeout = kwargs['timeout']

        self.session = requests.Session()
        if username is not None and password is not None:
            self.session.auth = (username, password)

        # if server url or timeout are not set, attempt to get from django settings
        if server_url is None or 'timeout' not in kwargs:
            try:
                from django.conf import settings
                if server_url is None:
                    server_url = self._serverurl_from_djangoconf()

                if 'timeout' not in kwargs:
                    timeout = getattr(settings, 'EXISTDB_TIMEOUT', None)
            except ImportError:
                pass


        # if server url is still not set, we have a problem
        if server_url is None:
            raise Exception('Cannot initialize an eXist-db connection without specifying ' +
                            'eXist server url directly or in Django settings as EXISTDB_SERVER_URL')

        # store for use with requests
        self.server_url = server_url

        # determine if we need http or https transport
        # (duplicates some logic in xmlrpclib)
        type, uri = splittype(server_url)
        if type not in ("http", "https"):
            raise IOError, "unsupported XML-RPC protocol"
        if type == 'https':
            transport = TimeoutSafeTransport(timeout=timeout, **datetime_opt)
        else:
            transport = TimeoutTransport(timeout=timeout, **datetime_opt)

        self.server = xmlrpclib.ServerProxy(
                uri="%s/xmlrpc" % server_url.rstrip('/'),
                transport=transport,
                encoding=encoding,
                verbose=verbose,
                allow_none=True,
                **datetime_opt
            )

    def _serverurl_from_djangoconf(self):
        # determine what exist url to use based on django settings, if available
        try:
            from django.conf import settings

            # don't worry about errors on this one - if it isn't set, this should fail
            exist_url = settings.EXISTDB_SERVER_URL

            # former syntax had credentials in the server url; warn about the change
            if '@' in exist_url:
                warnings.warn('EXISTDB_SERVER_URL should not include eXist user or ' +
                              'password information.  You should update your django ' +
                              'settings to use EXISTDB_SERVER_USER and EXISTDB_SERVER_PASSWORD.')

            # look for username & password
            username = getattr(settings, 'EXISTDB_SERVER_USER', None)
            password = getattr(settings, 'EXISTDB_SERVER_PASSWORD', None)

            # if username or password are configured, add them to the url
            if username or password:
                # split the url into its component parts
                urlparts = urlparse.urlsplit(exist_url)
                # could have both username and password or just a username
                if username and password:
                    # set auth in request session
                    self.session.auth = (username, password)

                    prefix = '%s:%s' % (username, password)
                else:
                    prefix = username
                # prefix the network location with credentials
                netloc = '%s@%s' % (prefix, urlparts.netloc)
                # un-split the url with all the previous parts and modified location
                exist_url = urlparse.urlunsplit((urlparts.scheme, netloc, urlparts.path,
                                                urlparts.query, urlparts.fragment))

            return exist_url
        except ImportError:
            pass

    def _path(self, path):
        # generate rest path to a collection or doucment
        # TODO: handle collection, extra slashes
        # FIXME: getting duplicated db path, handle this better
        if path.startswith('/db'):
            path = path[len('/db'):]
        return '%srest/db%s' % (self.server_url, path)

    def getDocument(self, name, **kwargs):
        """Retrieve a document from the database.

        :param name: database document path to retrieve
        :rtype: string contents of the document

        """
        logger.debug('getDocument %s' % self._path(name))
        response = self.session.get(self._path(name))
        # TODO: args ?
        print 'get document %s' % self._path(name)
        print response
        if response.status_code == requests.codes.ok:
            return response.content
        if response.status_code == requests.codes.not_found:
            # to match previous behavior;
            # TODO: use custom exception classes here
            raise exc.ExistDBException('%s not found' % name)


    def getDoc(self, name, **kwargs):
        "Alias for :meth:`getDocument`."
        return self.getDocument(name, **kwargs)


    def createCollection(self, collection_name, overwrite=False):
        """Create a new collection in the database.

        :param collection_name: string name of collection
        :param overwrite: overwrite existing document?
        :rtype: boolean indicating success

        """
        # FIXME: no longer relevant, since putting files creates collection?
        # TODO: use xmldb:create-collection via xquery

        # OR create by putting a file in the collection, then removing it?
        logger.debug('create collection %s' % collection_name)
        if not overwrite and self.hasCollection(collection_name):
            raise exc.ExistDBException(collection_name + " exists")

        response = self.session.put(self._path(collection_name))
        print 'create collection %s' % self._path(collection_name)
        print response
        return response.status_code == requests.codes.created

    def removeCollection(self, collection_name):
        """Remove the named collection from the database.

        :param collection_name: string name of collection
        :rtype: boolean indicating success

        """
        if (not self.hasCollection(collection_name)):
            raise exc.ExistDBException(collection_name + " does not exist")

        response = self.session.delete(self._path(collection_name))
        return response.status_code == requests.codes.ok

        # logger.debug('removeCollection %s' % collection_name)
        # return self.server.removeCollection(collection_name)

    def hasCollection(self, collection_name):
        """Check if a collection exists.

        :param collection_name: string name of collection
        :rtype: boolean

        """
        print 'head request on %s' % collection_name
        print self._path(collection_name)
        response = self.session.head(self._path(collection_name))
        # FIXME: need this somewhere reusable ...
        # TODO: also check 403 forbidden
        if response.status_code == requests.codes.unauthorized:
            raise exc.Unauthorized
        return response.status_code == requests.codes.ok

    def reindexCollection(self, collection_name):
        """Reindex a collection.
        Reindex will fail if the eXist user does not have the correct permissions
        within eXist (must be a member of the DBA group).

        :param collection_name: string name of collection
        :rtype: boolean success

        """
        if (not self.hasCollection(collection_name)):
            raise exc.ExistDBException(collection_name + " does not exist")

        # xquery reindex function requires that collection name begin with /db/
        if collection_name[0:3] != '/db':
            collection_name = '/db/' + collection_name.strip('/')

        result = self.query("xmldb:reindex('%s')" % collection_name)
        return result.values[0] == 'true'

    def hasDocument(self, document_path):
        """Check if a document is present in eXist.

        :param document_path: string full path to document in eXist
        :rtype: boolean

        """
        response = self.session.head(self._path(document_path))
        return response.status_code == requests.codes.ok

    @_wrap_xmlrpc_fault
    def describeDocument(self, document_path):
        """Return information about a document in eXist.
        Includes name, owner, group, created date, permissions, mime-type,
        type, content-length.
        Returns an empty dictionary if document is not found.

        :param document_path: string full path to document in eXist
        :rtype: dictionary

        """
        # TODO: not sure there is an equivalent in REST api,
        # although GET on collection might be sort of close

        logger.debug('describeResource %s' % document_path)
        return self.server.describeResource(document_path)

    def getCollectionDescription(self, collection_name):
        """Retrieve information about a collection.

        :param collection_name: string name of collection
        :rtype: boolean

        """
        logger.debug('getCollectionDesc %s' % collection_name)
        response = self.session.get(self._path(collection_name))
        if response.status_code == requests.codes.ok:
            return xmlmap.load_xmlobject_from_string(response.content, ResourceInfo)
        elif response.status_code == requests.codes.not_found:
            raise exc.ExistDBException('Collection %s not found' % collection_name)
        else:
            raise exc.ExistDBException

    def load(self, xml, path, overwrite=False):
        """Insert or overwrite a document in the database.

        :param xml: string or file object with the document contents
        :param path: destination location in the database
        :param overwrite: True to allow overwriting an existing document
        :rtype: boolean indicating success

        """
        if hasattr(xml, 'read'):
            xml = xml.read()

        logger.debug('load %s overwrite=%s' % (path, overwrite))
        # TODO: method to generate db path
        # NOTE: overwrite is assumed by REST
        response = self.session.put(self._path(path), xml)
        print response
        print response.content
        if response.status_code == requests.codes.bad_request:
            # response is HTML, not xml...
            # could use regex or beautifulsoup to pull out the error
            raise exc.ExistDBException
        return response.status_code == requests.codes.created

    def removeDocument(self, name):
        """Remove a document from the database.

        :param name: full eXist path to the database document to be removed
        :rtype: boolean indicating success

        """
        logger.debug('remove %s' % name)
        response = self.session.delete(self._path(name))
        return response.status_code == requests.codes.ok

    @_wrap_xmlrpc_fault
    def moveDocument(self, from_collection, to_collection, document):
        """Move a document in eXist from one collection to another.

        :param from_collection: collection where the document currently exists
        :param to_collection: collection where the document should be moved
        :param document: name of the document in eXist
        :rtype: boolean
        """
        self.query("xmldb:move('%s', '%s', '%s')" % \
                            (from_collection, to_collection, document))
        # query result does not return any meaningful content,
        # but any failure (missing collection, document, etc) should result in
        # an exception, so return true if the query completed successfully
        return True

    def query(self, xquery, start=1, how_many=10, cache=False,
             release=None, session=None, **kwargs):
        """Execute an XQuery query, returning the results directly.

        :param xquery: a string XQuery query
        :param start: first index to return (1-based)
        :param how_many: maximum number of items to return
        :rtype: the resultType specified at the creation of this ExistDB;
                defaults to :class:`QueryResult`.

        """
        logger.debug('query how_many=%d start=%d args=%s\n%s' % (how_many, start, kwargs, xquery))
        # xml_s = self.server.query(xquery, how_many, start, kwargs)
        params = {
                '_howmany': how_many,
                '_start': start,
                # kwargs??
        }
        if xquery is not None:
            params['_query'] = xquery
        if cache:
            params['_cache'] = 'yes'
        if release is not None:
            params['_release'] = release
        if session is not None:
            params['_session'] = session

        response = self.session.get(self._path(''), params=params)
        print response.content

        if response.status_code == requests.codes.ok:
            # TODO: test with unicode in return
            return xmlmap.load_xmlobject_from_string(response.content, self.resultType)

        # 400 bad request returns an xml error we can parse
        elif response.status_code == requests.codes.bad_request:
            err = xmlmap.load_xmlobject_from_string(response.content, ExistExceptionResponse)
            raise exc.ExistDBException(err.message)

        # not sure if any information is available on other error codes
        else:
            raise exc.ExistDBException

    @_wrap_xmlrpc_fault
    def executeQuery(self, xquery):
        """Execute an XQuery query, returning a server-provided result
        handle.

        :param xquery: a string XQuery query
        :rtype: an integer handle identifying the query result for future calls

        """
        logger.debug('executeQuery\n%s' % xquery)
        # we don't actually need any results, just the id, but
        # exist seems to ignore how_many=0
        result = self.query(xquery, how_many=1, cache=True)
        logger.debug('result id is %s' % result.session_id)
        return result.session_id

    @_wrap_xmlrpc_fault
    def querySummary(self, result_id):
        """Retrieve results summary from a past query.

        :param result_id: an integer handle returned by :meth:`executeQuery`
        :rtype: a dict describing the results

        The returned dict has four fields:

         * *queryTime*: processing time in milliseconds

         * *hits*: number of hits in the result set

         * *documents*: a list of lists. Each identifies a document and
           takes the form [`doc_id`, `doc_name`, `hits`], where:

             * *doc_id*: an internal integer identifier for the document
             * *doc_name*: the name of the document as a string
             * *hits*: the number of hits within that document

         * *doctype*: a list of lists. Each contains a doctype public
                      identifier and the number of hits found for this
                      doctype.

        """
        # FIXME: no exact equivalent in REST api;
        # in particular, no querytime
        print 'querysummary'
        result = self.query('', how_many=1, session=result_id)
        print result
        return result


        # FIXME: This just exposes the existdb xmlrpc querySummary function.
        #   Frankly, this return is just plain ugly. We should come up with
        #   something more meaningful.
        summary = self.server.querySummary(result_id)
        logger.debug('querySummary result id %d : ' % result_id + \
                     '%(hits)s hits, query took %(queryTime)s ms' % summary)
        return summary

    @_wrap_xmlrpc_fault
    def getHits(self, result_id):
        """Get the number of hits in a query result.

        :param result_id: an integer handle returned by :meth:`executeQuery`
        :rtype: integer representing the number of hits

        """
        result = self.querySummary(result_id)
        logger.debug('getHits result id %d : %s' % (result_id, result.hits))
        return result.hits

    @_wrap_xmlrpc_fault
    def retrieve(self, result_id, position, highlight=False, **options):
        """Retrieve a single result fragment.

        :param result_id: an integer handle returned by :meth:`executeQuery`
        :param position: the result index to return
        :param highlight: enable search term highlighting in result; optional,
            defaults to False
        :rtype: the query result item as a string

        """
        # TODO: equivalent in rest api?
        if highlight:
            # eXist highlight modes: attributes, elements, or both
            # using elements because it seems most reasonable default
            options['highlight-matches'] = 'elements'
            # pretty-printing with eXist matches can introduce unwanted whitespace
            if 'indent' not in options:
                options['indent'] = 'no'


        logger.debug('retrieve result id %d position=%d options=%s' % (result_id, position, options))
        return self.server.retrieve(result_id, position, options)

    @_wrap_xmlrpc_fault
    def releaseQueryResult(self, result_id):
        """Release a result set handle in the server.

        :param result_id: an integer handle returned by :meth:`executeQuery`

        """
        logger.debug('releaseQueryResult result id %d' % result_id)
        self.server.releaseQueryResult(result_id)

    @_wrap_xmlrpc_fault
    def setPermissions(self, resource, permissions):
        """Set permissions on a resource in eXist.

        :param resource: full path to a collection or document in eXist
        :param permissions: int or string permissions statement
        """
        # TODO: support setting owner, group ?
        # TODO: use xquery sm:chmod; see also chgrp, chown
        logger.debug('setPermissions %s %s' % (resource, permissions))
        self.server.setPermissions(resource, permissions)

    @_wrap_xmlrpc_fault
    def getPermissions(self, resource):
        """Retrieve permissions for a resource in eXist.

        :param resource: full path to a collection or document in eXist
        :rtype: ExistPermissions
        """
        # do we need this?

        # FIXME: no rest api equivalent, unless we use collection info
        # use xquery with sm:get-permissions(path)
        return ExistPermissions(self.server.getPermissions(resource))


    def loadCollectionIndex(self, collection_name, index, overwrite=True):
        """Load an index configuration for the specified collection.
        Creates the eXist system config collection if it is not already there,
        and loads the specified index config file, as per eXist collection and
        index naming conventions.

        :param collection_name: name of the collection to be indexed
        :param index: string or file object with the document contents (as used by :meth:`load`)
        :param overwrite: set to False to disallow overwriting current index (overwrite allowed by default)
        :rtype: boolean indicating success

        """
        index_collection = self._configCollectionName(collection_name)
        # FIXME: what error handling should be done at this level?
        print 'index collection = ', index_collection
        print 'index = ', index
        print 'collection index path = ', self._collectionIndexPath(collection_name)

        # create config collection if it does not exist
        # if not self.hasCollection(index_collection):
        #     self.createCollection(index_collection)

        # load index content as the collection index configuration file
        return self.load(index, self._collectionIndexPath(collection_name), overwrite)

    def removeCollectionIndex(self, collection_name):
        """Remove index configuration for the specified collection.
        If index collection has no documents or subcollections after the index
        file is removed, the configuration collection will also be removed.

        :param collection: name of the collection with an index to be removed
        :rtype: boolean indicating success

        """
        # collection indexes information must be stored under system/config/db/collection_name
        index_collection = self._configCollectionName(collection_name)

        # remove collection.xconf in the configuration collection
        self.removeDocument(self._collectionIndexPath(collection_name))

        desc = self.getCollectionDescription(index_collection)
        print desc.serialize(pretty=True)
        # no documents and no sub-collections - safe to remove index collection
        # FIXME: not sure rest api reports on subcollections
        # TODO: try xmldb:get-child-collections ?
        if not desc.collections and not desc.documents:
            self.removeCollection(index_collection)

        return True

    def hasCollectionIndex(self, collection_name):
        """Check if the specified collection has an index configuration in eXist.

        Note: according to eXist documentation, index config file does not *have*
        to be named *collection.xconf* for reasons of backward compatibility.
        This function assumes that the recommended naming conventions are followed.

        :param collection: name of the collection with an index to be removed
        :rtype: boolean indicating collection index is present

        """
        return self.hasCollection(self._configCollectionName(collection_name)) \
            and self.hasDocument(self._collectionIndexPath(collection_name))


    def _configCollectionName(self, collection_name):
        """Generate eXist db path to the configuration collection for a specified collection
        according to eXist collection naming conventions.
        """
        # collection indexes information must be stored under system/config/db/collection_name
        return "/db/system/config/db/" + collection_name.strip('/')

    def _collectionIndexPath(self, collection_name):
        """Generate full eXist db path to the index configuration file for a specified
        collection according to eXist collection naming conventions.
        """
        # collection indexes information must be stored under system/config/db/collection_name
        return self._configCollectionName(collection_name) + "/collection.xconf"

class ExistPermissions:
    "Permissions for an eXist resource - owner, group, and active permissions."
    def __init__(self, data):
        self.owner = data['owner']
        self.group = data['group']
        self.permissions = data['permissions']

    def __str__(self):
        return "owner: %s; group: %s; permissions: %s" % (self.owner, self.group, self.permissions)

    def __repr__(self):
        return '<%s %s>' % (self.__class__.__name__, str(self))


class QueryResult(xmlmap.XmlObject):
    """The results of an eXist XQuery query"""

    start = xmlmap.IntegerField("@exist:start")
    """The index of the first result returned"""

    values = xmlmap.StringListField("exist:value")
    "Generic value (*exist:value*) returned from an exist xquery"

    count = xmlmap.IntegerField("@exist:count")
    """The number of results returned in this chunk"""

    hits = xmlmap.IntegerField("@exist:hits")
    """The total number of hits found by the search"""

    session_id = xmlmap.IntegerField('@exist:session')
    'Session id, when using cached queries'

    @property
    def results(self):
        """The result documents themselves as nodes, starting at
        :attr:`start` and containing :attr:`count` members"""
        return self.node.xpath('*')

    # FIXME: Why do we have two properties here with the same value?
    # start == show_from. We should pick one and deprecate the other.
    @property
    def show_from(self):
        """The index of first object in this result chunk.

        Equivalent to :attr:`start`."""
        return self.start

    # FIXME: Not sure how we're using this, but it feels wonky. If we're
    # using it for chunking or paging then we should probably follow the
    # slice convention of returning the index past the last one. If we're
    # using it for pretty-printing results ranges then the rVal < 0 branch
    # sounds like an exception condition that should be handled at a higher
    # level. Regardless, shouldn't some system invariant handle the rVal >
    # self.hits branch for us? This whole method just *feels* weird. It
    # warrants some examination.
    @property
    def show_to(self):
        """The index of last object in this result chunk"""
        rVal = (self.start - 1) + self.count
        if rVal > self.hits:
            #show_to can not exceed total hits
            return self.hits
        elif rVal < 0:
            return 0
        else:
            return rVal

    # FIXME: This, too, feels like it checks a number of things that should
    # probably be system invariants. We should coordinate what this does
    # with how it's actually used.
    def hasMore(self):
        """Are there more matches after this one?"""
        if not self.hits or not self.start or not self.count:
            return False
        return self.hits > (self.start + self.count)

class ExistExceptionResponse(xmlmap.XmlObject):
    '''XML exception response returned on an error'''
    #: db path where the error occurred
    path = xmlmap.StringField('path')
    #: error message
    message = xmlmap.StringField('message')
    #: query that generated the error
    query = xmlmap.StringField('query')


class ResourceInfo(xmlmap.XmlObject):
    'Resource information for a collection'
    name = xmlmap.StringField('exist:collection/@name')
    created = xmlmap.DateTimeField('exist:collection/@created')
    owner = xmlmap.StringField('exist:collection/@owner')
    group = xmlmap.StringField('exist:collection/@group')
    permissions = xmlmap.StringField('exist:collection/@permissions')
    #: note permissions are in this format:   permissions="rwxr-xr-x"
    documents = xmlmap.NodeListField('exist:collection/exist:resource', 'self')
    # TODO: test that subcollections look like this
    collections = xmlmap.NodeListField('exist:collection/exist:collections', 'self')


# Custom xmlrpclib Transport classes for configurable timeout
# Initially adapted from code found here:
# http://stackoverflow.com/questions/372365/set-timeout-for-xmlrpclib-serverproxy

# NOTE: TimeoutHTTP and TimeoutHTTPS are needed for compatibility with
# Python 2.6 and earlier (see UGLY HACK ALERT below). They are not used in
# Python 2.7 and newer.
class TimeoutHTTP(httplib.HTTP):
    def __init__(self, host='', port=None, strict=None, timeout=None):
         if port == 0:
             port = None
         self._setup(self._connection_class(host, port, strict, timeout))

class TimeoutHTTPS(httplib.HTTPS):
    def __init__(self, host='', port=None, strict=None, timeout=None):
         if port == 0:
             port = None
         self._setup(self._connection_class(host, port, strict, timeout))

class TimeoutTransport(xmlrpclib.Transport):
    '''Extend the default :class:`xmlrpclib.Transport` to expose a
    connection timeout parameter.'''
    # UGLY HACK ALERT. Python 2.6 wants make_connection to return something
    # that looks like a httplib.HTTP. Python 2.7 wants a
    # httplib.HTTPConnection. We use an ugly hack (commented below) to
    # figure out which environment we're running in. _http_connection is
    # used for 2.7-style connections; _http_connection_compat is used for
    # 2.6-style.
    _http_connection = httplib.HTTPConnection
    _http_connection_compat = TimeoutHTTP

    def __init__(self, timeout=None, *args, **kwargs):
        if timeout is None:
            timeout = socket._GLOBAL_DEFAULT_TIMEOUT
        xmlrpclib.Transport.__init__(self, *args, **kwargs)
        self.timeout = timeout

        # UGLY HACK ALERT. If we're running on Python 2.6 or earlier,
        # self.make_connection() needs to return an HTTP; newer versions
        # expect an HTTPConnection. Our strategy is to guess which is
        # running, and override self.make_connection for older versions.
        # That check and override happens here.
        if self._connection_requires_compat():
            self.make_connection = self._make_connection_compat

    def _connection_requires_compat(self):
        # UGLY HACK ALERT. Python 2.7 xmlrpclib caches connection objects in
        # self._connection (and sets self._connection in __init__). Python
        # 2.6 and earlier has no such cache. Thus, if self._connection
        # exists, we're running the newer-style, and if it doesn't then
        # we're running older-style and thus need compatibility mode.
        try:
            self._connection
            return False
        except AttributeError:
            return True

    def make_connection(self, host):
        # This is the make_connection that runs under Python 2.7 and newer.
        # The code is pulled straight from 2.7 xmlrpclib, except replacing
        # HTTPConnection with self._http_connection
        if self._connection and host == self._connection[0]:
            return self._connection[1]
        chost, self._extra_headers, x509 = self.get_host_info(host)
        self._connection = host, self._http_connection(chost, timeout=self.timeout)
        return self._connection[1]

    def _make_connection_compat(self, host):
        # This method runs as make_connection under Python 2.6 and older.
        # __init__ detects which version we need and pastes this method
        # directly into self.make_connection if necessary.
        host, extra_headers, x509 = self.get_host_info(host)
        return self._http_connection_compat(host, timeout=self.timeout)


class TimeoutSafeTransport(TimeoutTransport):
    '''Extend class:`TimeoutTransport` but use HTTPS connections;
    timeout-enabled equivalent to :class:`xmlrpclib.SafeTransport`.'''
    _http_connection = httplib.HTTPSConnection
    _http_connection_compat = TimeoutHTTPS

