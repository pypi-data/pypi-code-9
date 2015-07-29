# Copyright (c) 2011-2013 Rackspace Hosting
# All Rights Reserved.
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""MongoDB backend wrapper."""

from __future__ import print_function

import copy
import json
import logging

try:
    import eventlet
except ImportError:
    pass
import pymongo
from pymongo.son_manipulator import SONManipulator

from simpl.db import reconnector
from simpl import log
from simpl import secrets

LOG = logging.getLogger(__name__)


class SimplDBError(Exception):

    """Any DB Exception."""


class SimplMongoError(SimplDBError):

    """MongoDB Exception."""


class ValidatonError(Exception):

    """Failed Input Validation."""


def scrub(data):
    """Verify and clean data. Raise error if input fails."""
    # blanks, Nones, and empty strings can stay as is
    if not data:
        return data
    if isinstance(data, (type(None), int, float)):
        return data
    if isinstance(data, list):
        return [scrub(entry) for entry in data]
    if isinstance(data, dict):
        return {scrub(key): scrub(value) for key, value in data.iteritems()}
    try:
        return json.encoder.encode_basestring(data)[1:-1]
    except TypeError as exc:
        raise ValidatonError("Input '%s' is not a permitted type: %s" % (data,
                                                                         exc))
    except Exception as exc:
        raise ValidatonError("Input '%s' not permitted: %s" % (data, exc))


class SimplDB(object):

    """Database wrapper.

    This Database wrapper disables a SONManipulator that is
    normally enabled through pymongo by default. That manipulator
    is found at pymongo.son_manipulator.ObjectIdInjector

    With the injector disabled, if you were to write a document,
    have manipulate=True AND *not* provide an _id, you wouldn't
    see an insert confirmation, and pymongo does not
    inform you of the objectid for the document that was inserted.

    We think the purpose of that manipulator was to enable pymongo
    to always return a write confirmation that was associated with a
    particular object id, where that object id could be generated
    *by* pymongo (using ObjectIdInjector) *before* inserting the document.

    This caused a couple problems:
        1. When performing a partial update of a document,
           if you did not provide the _id with the data,
           pymongo would generate a new one, and whatever
           document you were pointing to (based on a spec)
           would have its _id overwritten.
        2. Typically, we would not reach (1), because a
           partial update will make use of the $set operator,
           (or any operator) and pymongo would add the _id to
           that set of data, creating a document that would
           look something like this:
                * {'$set': {'data.to.update': 'yes'},
                   '_id': ObjectId('530264af09df64dd0235b155')}
           where you would receive the following error:

            pymongo.errors.OperationFailure: Modifiers and non-modifiers
                                             cannot be mixed

    """

    __collections__ = tuple()

    def __init__(self, config):
        """Initialize database wrapper."""
        self.config = config
        self.connection_string = self.config['connection_string']
        self.safe_connection_string = secrets.hide_url_password(
            self.connection_string)
        parsed = pymongo.uri_parser.parse_uri(self.connection_string)
        self.database_name = parsed.get('database') or 'waldo'
        self._client = None
        self._connection = None
        eventlet.spawn_n(self.tune)

    @property
    def client(self):
        """Return a lazy-instantiated pymongo client."""
        block = eventlet.semaphore.Semaphore(id(self))
        with block:
            if self._client is None:
                self._client = pymongo.MongoClient(self.connection_string)
                LOG.debug("Created new connection to MongoDB: %s",
                          self.safe_connection_string)
        return self._client

    @property
    def connection(self):
        """Connect to and return mongodb database object."""
        if self._connection is None:

            self._connection = reconnector.MongoProxy(
                self.client[self.database_name], logger=LOG)

            # pymongo/database.py includes ObjectIdInjector manipulator
            # by default. Here, we are resetting the manipulators b/c
            # we don't want the ObjectIdInjector to add an `_id` to
            # our modifiers.

            for manip in self._connection._Database__incoming_manipulators:
                if isinstance(manip, pymongo.son_manipulator.ObjectIdInjector):
                    self._connection._Database__incoming_manipulators.remove(
                        manip)
                    LOG.debug("Disabling %s on mongodb connection to '%s'.",
                              manip.__class__.__name__, self.database_name)
                    break

            self._connection.add_son_manipulator(KeyTransform(".", "_dot_"))
            self._connection.add_son_manipulator(ObjectSerializer())
            LOG.info("Connected to mongodb on %s (database=%s)",
                     self.safe_connection_string, self.database_name)

        return self._connection

    def tune(self):
        """Documenting & Automating Index Creation."""
        LOG.debug("Tuning database")

        conn = self.connection

        def create_index(collection, index_name, **kwargs):
            try:
                conn[collection].create_index(index_name, **kwargs)
            except Exception as exc:
                LOG.warn("Error tuning mongodb database | %s",
                         log.pytb_lastline(exc))

        #
        # Audits
        #
        create_index('audits', "event",
                     background=True,
                     name="audits_event")

        #
        # Applications
        #
        # Search for applictions by customer.
        create_index('applications', "customer_id",
                     background=True,
                     name="applications_customer_id")
        # Support q= text indexing on select fields
        create_index('applications',
                     [("name", pymongo.TEXT),
                      ("url", pymongo.TEXT),
                      ("keywords", pymongo.TEXT)],
                     background=True,
                     name="applications_q",
                     default_language="none")  # include stop words like "Do"
        # required to search for partial name along with text index
        create_index('applications', "name",
                     background=True,
                     name="applications_name")
        create_index('applications', "facets",
                     background=True,
                     name="applications_facets")

        #
        # Customers
        #
        # Support q= text indexing on select fields
        create_index('customers',
                     [("name", pymongo.TEXT),
                      ("team", pymongo.TEXT),
                      ("keywords", pymongo.TEXT),
                      ("core_account_number", pymongo.TEXT),
                      ("account_manager.email", pymongo.TEXT),
                      ("account_manager.name", pymongo.TEXT),
                      ("business_development_consultant.email", pymongo.TEXT),
                      ("business_development_consultant.name", pymongo.TEXT)],
                     background=True,
                     name="customer_q",
                     default_language="none")  # include stop words like "Do"
        # required to search for partial name along with text index
        create_index('customers', "name",
                     background=True,
                     name="customer_name")
        create_index('customers', "facets",
                     background=True,
                     name="customer_facets")

        #
        # Stacks
        #
        # Support q= text indexing on select fields
        create_index('stacks',
                     [("name", pymongo.TEXT),
                      ("keywords", pymongo.TEXT),
                      ("github_repo_url", pymongo.TEXT)],
                     background=True,
                     name="stack_q",
                     default_language="none")  # include stop words like "Do"
        # required to search for partial name along with text index
        create_index('stacks', "name",
                     background=True,
                     name="stack_name")
        create_index('stacks', "facets",
                     background=True,
                     name="stack_facets")

        #
        # Discoveries
        #
        create_index('discoveries', "netloc",
                     background=True,
                     name="discoveries_netloc")
        create_index('discoveries', [("time", pymongo.DESCENDING)],
                     background=True,
                     name="discoveries_time")
        create_index('discoveries', "created_by",
                     background=True,
                     name="discoveries_created_by")

        #
        # Resources
        #
        create_index('resources', "tenant_id",
                     background=True,
                     name="resources_tenant_id")
        create_index('resources', "netlocs",
                     background=True,
                     name="resources_netlocs")
        create_index('resources', "updated",
                     background=True,
                     name="resources_updated")

    def __getattr__(self, key):
        """Access the Collection attribute of the database connector."""
        if key in self.__collections__:
            return Collection(self.connection, key.lower())
        else:
            raise AttributeError("SimplDB does not have attribute '%s'" % key)


class Collection(object):

    """Wrapper for a collection."""

    def __init__(self, connection, collection_name):
        """Initialize collection wrapper."""
        self.connection = connection
        self.collection_name = collection_name
        self._collection = self.connection[collection_name]

        # Wrap _list() call to handle cursor AutoReconnect exceptions.
        # Unlike most other calls, cursors proved to be difficult to wrap in a
        # MongoProxy (reconnects were handled correctly, but `limit` was no
        # longer honored).
        self.list = reconnector.Executable(self.list, LOG)

    def save(self, key, data):
        """Create or Save a document in a collection.

        :returns: count of records added/updated
        """
        write = data.copy()
        write['_id'] = key
        response = self._collection.update({'_id': key}, write, upsert=True,
                                           manipulate=True)
        if response.get('ok') != 1:
            raise SimplMongoError("Error saving document '%s': %s" % (
                                  key, response.errmsg))
        LOG.debug("DB WRITE: %s.%s", self.collection_name, response)
        return response.get('n')

    def update_multi(self, data, **kwargs):
        """Partial update (by kwarg filter) of document(s).

        The filter to match documents is built from kwargs.
        Requires at least one kwarg to build a filter.

        'data' AND/OR kwarg filter(s) may contain dot notation
        fields, in order to specify nested values in the documents, e.g.

            collection.update({'datatowrite': 'yes'},
                              **{'my.nested.field': 'match!'})

        The dictionary provided as 'data' will update only
        those corresponding fields and subfields in the database
        document, without clobbering other fields and
        subfields.
        """
        if not kwargs:
            raise TypeError("update() requires at least one "
                            "kwarg to build a filter (0 given).")

        spec = kwargs
        write = data.copy()

        response = self._collection.update(
            spec, {'$set': write}, multi=True, upsert=False, manipulate=True)

        if response.get('ok') != 1:
            raise SimplMongoError("Error updating document '%s': %s" % (
                                  spec.get('_id'), response.errmsg))
        LOG.debug("DB UPDATE: %s.%s", self.collection_name, response)
        return response.get('n')

    def update(self, key, data):
        """Update document by key with partial data.

        Updates the document matching _id=<key> with 'data'
            Where 1st argument 'key' is <key>

        'data' may contain dot notation fields in
        order to specify nested values in the documents, e.g.

            collection.update(<document_key>,
                              {'my.nested.field': 'match!'})

        The dictionary provided as 'data' will update only
        those corresponding fields and subfields in the database
        document, without clobbering other fields and
        subfields.

        :returns: count of records added/updated
        """
        if key:
            spec = {'_id': key}

        write = data.copy()

        response = self._collection.update(
            spec, {'$set': write}, multi=False, upsert=False, manipulate=True)

        if response.get('ok') != 1:
            raise SimplMongoError("Error updating document '%s': %s" % (
                                  spec.get('_id'), response.errmsg))
        LOG.debug("DB UPDATE: %s.%s", self.collection_name, response)
        return response.get('n')

    def count(self):
        """Number of documents in a collection."""
        return self._collection.count()

    def list(self, offset=0, limit=0, fields=None, sort=None, **kwargs):
        """Return filtered list of documents in a collection.

        :param offset: for pagination, which record to start attribute
        :param limit: for pagination, how many records to return
        :param fields: list of field names to return (otherwise returns all)
        :param sort: list of fields to sort by (prefix with '-' for descending)
        :param kwargs: key/values to find (only supports equality for now)

        :returns: a tuple of the list of documents and the total count
        """
        try:
            cursor = self._cursor(offset=offset, limit=limit, fields=fields,
                                  sort=sort, **kwargs)
            return list(cursor), cursor.count()
        except pymongo.errors.OperationFailure as exc:
            # This is workaround for mongodb v2.4 and 'q' filter params
            try:
                kwargs['$or'][0]['$text']['$search']
            except (KeyError, IndexError):
                raise exc
            LOG.warn("Falling back to hard-coded mongo v2.4 search behavior")
            kwargs = self.search_alternative(limit, **kwargs)
            LOG.debug("Modified kwargs: %s", kwargs)
            cursor = self._cursor(offset=offset, limit=limit, fields=fields,
                                  sort=sort, **kwargs)
            return list(cursor), cursor.count()

    def search_alternative(self, limit, **kwargs):
        """Replace $search with $in for mongodb v2.4.

        This is a workaround for mongo v2.4 not supporting the $search keyword.
        This workaround is hardcoded specifically for the 'q' query param. The
        text search is executed first and the ids of the found documents are
        used to replace the $search filter with a $in filter.
        """
        search_term = kwargs['$or'][0]['$text']['$search']
        response = self._collection.database.command(
            'text', self._collection.name,
            search=search_term,
            project={'_id': 1},
            limit=limit
        )
        id_list = [e['obj']['_id'] for e in response['results']]
        kwargs['$or'][0] = {'_id': {'$in': id_list}}
        return kwargs

    def _cursor(self, offset=0, limit=0, fields=None, sort=None, **kwargs):
        """Return a cursor on a filtered list of documents in a collection.

        :param offset: for pagination, which record to start attribute
        :param limit: for pagination, how many records to return
        :param fields: list of field names to return (otherwise returns all)
        :param sort: list of fields to sort by (prefix with '-' for descending)
        :param kwargs: key/values to find (only supports equality for now)

        :returns: a tuple of a cursor on documents and the total count

        Note: close the cursor after using it if you don't exhaust it
        """
        projection = {'_id': False}
        if fields:
            projection.update({field: True for field in fields})
        results = self._collection.find(spec=kwargs, fields=projection)
        if sort:
            sort_pairs = sort[:]
            for index, field in enumerate(sort):
                if field[0] == "-":
                    sort_pairs[index] = (field[1:], pymongo.DESCENDING)
                else:
                    sort_pairs[index] = (field, pymongo.ASCENDING)
            results.sort(sort_pairs)
        results.skip(offset or 0).limit(limit or 0)
        return results

    def delete(self, key):
        """Delete a document by id."""
        assert key, "A key must be supplied for delete operations"
        self._collection.remove(spec_or_id={'_id': key})
        LOG.debug("DB REMOVE: %s.%s", self.collection_name, key)

    def exists(self, key):
        """True if a document exists."""
        try:
            return self._collection.find_one({'_id': key}) is not None
        except StopIteration:
            return False

    def get(self, key):
        """Get a document by id."""
        doc = self._collection.find_one({'_id': key})
        if doc:
            doc.pop('_id')
            return doc


class KeyTransform(SONManipulator):

    """Transforms keys going to database and restores them coming out.

    This allows keys with dots in them to be used (but does break searching on
    them unless the find command also uses the transform).

    Example & test:
        # To allow `.` (dots) in keys
        import pymongo
        client = pymongo.MongoClient("mongodb://localhost")
        db = client['delete_me']
        db.add_son_manipulator(KeyTransform(".", "_dot_"))
        db['mycol'].remove()
        db['mycol'].update({'_id': 1}, {'127.0.0.1': 'localhost'}, upsert=True,
                           manipulate=True)
        print db['mycol'].list().next()
        print db['mycol'].list({'127_dot_0_dot_0_dot_1': 'localhost'}).next()

    Note: transformation could be easily extended to be more complex.
    """

    def __init__(self, replace, replacement):
        """Initialize KeyTransform."""
        self.replace = replace
        self.replacement = replacement

    def transform_key(self, key):
        """Transform key for saving to database."""
        return key.replace(self.replace, self.replacement)

    def revert_key(self, key):
        """Restore transformed key returning from database."""
        return key.replace(self.replacement, self.replace)

    def transform_incoming(self, son, collection):
        """Recursively replace all keys that need transforming."""
        return self._transform_incoming(copy.deepcopy(son), collection)

    def _transform_incoming(self, son, collection, skip=0):
        """Recursively replace all keys that need transforming."""
        skip = 0 if skip < 0 else skip
        if isinstance(son, dict):
            for (key, value) in son.items():
                if key.startswith('$'):
                    if isinstance(value, dict):
                        skip = 2
                    else:
                        pass  # allow mongo to complain
                if self.replace in key:
                    k = key if skip else self.transform_key(key)
                    son[k] = self._transform_incoming(
                        son.pop(key), collection, skip=skip - 1)
                elif isinstance(value, dict):  # recurse into sub-docs
                    son[key] = self._transform_incoming(value, collection,
                                                        skip=skip - 1)
                elif isinstance(value, list):
                    son[key] = [
                        self._transform_incoming(k, collection, skip=skip - 1)
                        for k in value
                    ]
            return son
        elif isinstance(son, list):
            return [self._transform_incoming(item, collection, skip=skip - 1)
                    for item in son]
        else:
            return son

    def transform_outgoing(self, son, collection):
        """Recursively restore all transformed keys."""
        if isinstance(son, dict):
            for (key, value) in son.items():
                if self.replacement in key:
                    k = self.revert_key(key)
                    son[k] = self.transform_outgoing(son.pop(key), collection)
                elif isinstance(value, dict):  # recurse into sub-docs
                    son[key] = self.transform_outgoing(value, collection)
                elif isinstance(value, list):
                    son[key] = [self.transform_outgoing(item, collection)
                                for item in value]
            return son
        elif isinstance(son, list):
            return [self.transform_outgoing(item, collection)
                    for item in son]
        else:
            return son


class ObjectSerializer(SONManipulator):

    """Serialize Simpl objects in the database layer."""

    def transform_incoming(self, son, collection):
        """Recursively replace all keys that need transforming.

        This will serialize all objects that have a
        serialize method before sending them to mongo.

        """
        for (key, value) in son.items():
            if isinstance(value, dict):  # Make sure we recurse into sub-docs
                son[key] = self.transform_incoming(value, collection)
            elif hasattr(value, 'serialize'):
                LOG.debug("Serializing object: %s", value)
                son[key] = value = value.serialize()
        return son


def database(conf):
    """Return database singleton instance.

    This function will always return the same database instance for the same
    config. It stores instances in a dict saved as an attribute of this
    function.
    """
    if not hasattr(database, "singletons"):
        database.singletons = {}
    try:
        key = hash(conf)
    except TypeError:
        key = id(conf)
    if key not in database.singletons:
        instance = SimplDB(conf)
        database.singletons[key] = instance
    return database.singletons[key]


def test():
    """Just a quick test."""
    from waldo.common import config
    conf = config.current()
    conf.connection_string = "mongodb://localhost/delete_me"
    wdb = database(conf)
    print("Connections:", wdb.client, wdb.connection)
    wdb.connection.discoveries.remove()
    wdb.connection.dossiers.remove()
    print("Inserted %s record" % wdb.discoveries.save("A", {"name": "test A"}))
    print("Inserted %s record" % wdb.discoveries.save("B", {"name": "test B"}))
    print("Inserted %s record" % wdb.discoveries.save("Z", {"name": "test Z"}))
    print("Inserted %s record" % wdb.discoveries.save("D", {"name": "test D"}))
    print("List:", wdb.discoveries.list())
    print("Page:", wdb.discoveries.list(offset=1, limit=2)[0])
    print("Find 'D':", list(wdb.discoveries.list(name="test D", limit=1)[0]))
    wdb.discoveries.delete("D")
    print("Latest:", wdb.discoveries.list(limit=1, sort=["-name"])[0])
    print("First:", wdb.discoveries.list(limit=1, sort=["name"])[0])

    print("Delete 'D' then find it again:",
          wdb.discoveries.list(name="test D", limit=1))
    print("Count:", wdb.discoveries.count())
    wdb.discoveries._collection.remove()  # pylint: disable=W0212
    print("Cleared:", wdb.discoveries.count())

    wdb.dossiers.save("foo", {'netloc': 'localhost'})
    wdb.dossiers.save("bar", {'netloc': 'localhost', 'foo': 12})
    wdb.dossiers.save("zap", {'netloc': 'google.com'})

    print("Found:", wdb.dossiers.list(foo=12)[0])
    print("zap Exists:", wdb.dossiers.exists("zap"))
    print("wop Exists:", wdb.dossiers.exists("wop"))
    print("zap:", wdb.dossiers.get("zap"))
    print("wop:", wdb.dossiers.get("wop"))

    wdb.dossiers.save("dot", {'127.0.0.1': {'server.local': 'for example'}})
    print("Restore recursive dots:", wdb.dossiers.get("dot"))
    data = {'server.local': 'does this work'}
    wdb.dossiers.save('Y', data)
    print("Data unchanged:", data == {'server.local': 'for example'})
    print("Find w/ dots:",
          wdb.dossiers.list(server_dot_local='does this work'))

    print("Recurse through dicts AND lists to transform keys!")
    lods = {'addresses': [{'127.0.0.1': 'for example'},
                          {'127.0.0.2': 'another'}]}
    wdb.dossiers.save("nope", lods)
    returned = wdb.dossiers.get('nope')
    print("Restore recursive dots in list of dicts:", returned)
    assert lods == returned, ("RETURNED: %s\n !=\n WRITTEN: %s"
                              % (returned, lods))
    data = {'server.local': 'for example'}
    wdb.dossiers.save('X', data)
    print("Data unchanged:", data == {'server.local': 'for example'})
    assert data == wdb.dossiers.get('X')
    print("Find w/ dots:",
          wdb.dossiers.list(server_dot_local='for example'))

    data = {'nmbrz': [1, 2, 3, 4, 5, 6]}
    wdb.dossiers.save("numlist", data)
    again = wdb.dossiers.get("numlist")
    print("Restore numlist:", again)
    print("Data unchanged:", data == again)

    record = {"yes": "Show it", "no": "don't show it"}
    print("Inserted %s record" % wdb.discoveries.save("X", record))
    print("List all field:", wdb.discoveries.list()[0])
    print("List one field:", wdb.discoveries.list(fields=['yes'])[0])

    print("\nTesting 02/17/2014 update()")
    record = {"momo": "record", "update_me": "yes"}
    print("Momo Record:", record)
    print("Inserting Momo Record (will update on next call):",
          wdb.dossiers.save("momokey", record))
    print("Getting newly inserted Momo Record:",
          wdb.dossiers.list(_id="momokey")[0])
    print("Updating (by key) Momo Record:",
          wdb.dossiers.update("momokey", {"update_me": "by_golly"}))
    print("Getting updated (by key) Momo Record:",
          wdb.dossiers.get("momokey"))
    print("Updating (by kwarg filter) Momo Record:",
          wdb.dossiers.update_multi({"update_me": "what_the_what"},
                                    update_me="by_golly"))
    print("Getting updated (by kwarg filter) Momo Record:",
          wdb.dossiers.get("momokey"))

    print("\nTest case: avoiding KeyTransform when key.startswith('$')")
    print('\n(1) Testing dot.notation usage of update()')
    record = {'this': {'that': 'theother'}}
    print("Inserting Fantasm document %s with nested values:" % record,
          wdb.dossiers.save("fantasm", record))
    print("Getting newly inserted Fantasm record:",
          wdb.dossiers.list(_id="fantasm")[0])
    print("Updating (by dot.notation key) Fantasm Record:",
          wdb.dossiers.update("fantasm", {"this.that": "by_golly"}))
    print("Getting updated (by dot.notation key) Fantasm Record:",
          wdb.dossiers.get("fantasm"))
    kwfilter = {'this.that': 'by_golly'}
    print("Updating (by dot.notation kwarg filter) Fantasm Record:",
          wdb.dossiers.update_multi({"this.that": "what_the_what"},
                                    **kwfilter))
    print("Getting updated (by dot.notation kwarg filter) Fantasm Record:",
          wdb.dossiers.get("fantasm"))

    wdb.connection.dossiers.remove()
    print("\nTest case: avoiding KeyTransform when key.startswith('$')")
    print("(2) First field after operator has no '.', transform subsequent")
    record = {'this': {'that': 'theother'}}
    print("Inserting Fantasm document %s with nested values:" % record,
          wdb.dossiers.save("fantasm", record))
    print("Getting newly inserted Fantasm record:",
          wdb.dossiers.list(_id="fantasm")[0])
    print("Updating (by dot.notation key) Fantasm Record:",
          wdb.dossiers.update("fantasm",
                              {"this": {"the.other": {"by": "golly"}}}))
    print("Getting updated (by dot.notation key) Fantasm Record:",
          wdb.dossiers.get("fantasm"))
    kwfilter = {'this': {'the_dot_other': {'by': 'golly'}}}
    print("Kwarg filter here knows about KeyTransform, otherwise\n"
          "we have to transform search keys anytime you want to\n"
          "search for a field whose key has been transformed.")
    print("kwarg filter: %s" % kwfilter)
    print("Updating (by dot.notation kwarg filter) Fantasm Record:",
          wdb.dossiers.update_multi(
              {'this': {'the.other': {'by': 'what_the_what'}}}, **kwfilter))
    print("Getting updated (by dot.notation kwarg filter) Fantasm Record:",
          wdb.dossiers.get("fantasm"))

    wdb.connection.dossiers.remove()
    print("\nTest case: avoiding KeyTransform when key.startswith('$')")
    print("(3) Adjacent dot-notation and dot in field name")
    record = {'this': {'that': 'theother'}}
    print("Inserting Fantasm document %s with nested values:" % record,
          wdb.dossiers.save("fantasm", record))
    print("Getting newly inserted Fantasm record:",
          wdb.dossiers.list(_id="fantasm")[0])
    print("Updating (by dot.notation key) Fantasm Record:",
          wdb.dossiers.update("fantasm",
                              {"this.that": {"the.other": {"by": "golly"}}}))
    print("Getting updated (by dot.notation key) Fantasm Record:",
          wdb.dossiers.get("fantasm"))
    kwfilter = {'this.that': {'the_dot_other': {'by': 'golly'}}}
    print("Kwarg filter here knows about KeyTransform, otherwise\n"
          "we have to transform search keys anytime you want to\n"
          "search for a field whose key has been transformed.")
    print("kwarg filter: %s" % kwfilter)
    print("Updating (by dot.notation kwarg filter) Fantasm Record:",
          wdb.dossiers.update_multi(
              {'this.that': {'the.other': {'by': 'what_the_what'}}},
              **kwfilter))
    print("Getting updated (by dot.notation kwarg filter) Fantasm Record:",
          wdb.dossiers.get("fantasm"))

    wdb.connection.dossiers.remove()
    print("\nTest case: Nest Further")
    record = {'one': {'two': {'three': {'four': 'ok'}}}}
    print("Inserting Fantasm document %s with nested values:" % record,
          wdb.dossiers.save("fantasm", record))
    print("Getting newly inserted Fantasm record:",
          wdb.dossiers.list(_id="fantasm")[0])
    print("Updating (by dot.notation key) Fantasm Record:",
          wdb.dossiers.update("fantasm",
                              {"one.two.three.four": {"five": "ok"}}))
    print("Getting updated (by dot.notation key) Fantasm Record:",
          wdb.dossiers.get("fantasm"))
    assert ({'one': {'two': {'three': {'four': {'five': 'ok'}}}}} ==
            wdb.dossiers.get('fantasm'))
    kwfilter = {'one.two.three.four.five': 'ok'}
    print("kwarg filter: %s" % kwfilter)
    print("Updating (by dot.notation kwarg filter) Fantasm Record:",
          wdb.dossiers.update_multi({"one.two.three.four.five": "good",
                                     "new.field": "newvalue"}, **kwfilter))
    print("Getting updated (by dot.notation kwarg filter) Fantasm Record:",
          wdb.dossiers.get("fantasm"))
    assert ({'new': {'field': 'newvalue'},
             'one': {'two': {'three': {'four': {'five': 'good'}}}}} ==
            wdb.dossiers.get('fantasm'))

    print("\nObjectIdInjector's removal is hard-coded into our SimplDB class.")
    foodoc = {"foo": "bar"}
    print("Test saving a new document %s without specifying an _id:" % foodoc,
          wdb.dossiers._collection.insert(foodoc))
    print("Can we find document %s? :" % foodoc,
          wdb.dossiers.list(foo="bar", fields=["_id", "foo"]))
    print("\n### N.B. ###")
    print("MongoDB generated & assigned our document an _id even\nwithout "
          "pymongo's ObjectIdInjector, but returns None\ninstead of that "
          "objectid when inserting the new document.")

if __name__ in ["__main__", "__live_coding__"]:
    test()
