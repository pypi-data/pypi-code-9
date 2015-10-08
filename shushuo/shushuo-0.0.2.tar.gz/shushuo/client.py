import copy
import sys
from shushuo import persistence_strategies, exceptions
from shushuo.api import ShushuoApi
from shushuo.persistence_strategies import BasePersistenceStrategy


class Event(object):
    """
    An event in Shushuo.
    """

    def __init__(self, project_id, event_collection, event_body,
                 timestamp=None):
        """ Initializes a new Event.

        :param project_id: the Shushuo project ID to insert the event to
        :param event_collection: the Shushuo collection name to insert the event to
        :param event_body: a dict that contains the body of the event to insert
        :param timestamp: optional, specify a datetime to override the
        timestamp associated with the event in Shushuo
        """
        super(Event, self).__init__()
        self.project_id = project_id
        self.event_collection = event_collection
        self.event_body = event_body
        self.timestamp = timestamp

    def to_json(self):
        """ Serializes the event to JSON.

        :returns: a string
        """
        event_as_dict = copy.deepcopy(self.event_body)
        if self.timestamp:
            event_as_dict["meta"] = {"timestamp": self.timestamp.isoformat()}
        return event_as_dict


class ShuClient(object):
    """ The Shushuo Client is the main object to use to interface with Shushuo. It
    requires a project ID and one or both of write_key and read_key.

    Optionally, you can also specify a persistence strategy to elect how
    events are handled when they're added. The default strategy is to send
    the event directly to Shushuo, in-line. This may not always be the best
    idea, though, so we support other strategies (such as persisting
    to a local Redis queue for later processing).

    GET requests will timeout after 305 seconds by default.

    POST requests will timeout after 305 seconds by default.
    """

    def __init__(self, project_id, write_key=None, read_key=None, base_url=None,
                 persistence_strategy=None, api_class=ShushuoApi, get_timeout=305, post_timeout=305,
                 master_key=None):
        """ Initializes a ShuClient object.

        :param project_id: the Shushuo IO project ID
        :param write_key: a Shushuo IO Scoped Key for Writes
        :param read_key: a Shushuo IO Scoped Key for Reads
        :param persistence_strategy: optional, the strategy to use to persist
        the event
        :param get_timeout: optional, the timeout on GET requests
        :param post_timeout: optional, the timeout on POST requests
        :param master_key: a Shushuo IO Master API Key
        """
        super(ShuClient, self).__init__()

        # do some validation
        self.check_project_id(project_id)

        # Set up an api client to be used for querying and optionally passed
        # into a default persistence strategy.
        self.api = api_class(project_id, write_key=write_key, read_key=read_key,
                             base_url=base_url, get_timeout=get_timeout, post_timeout=post_timeout,
                             master_key=master_key)

        if persistence_strategy:
            # validate the given persistence strategy
            if not isinstance(persistence_strategy, BasePersistenceStrategy):
                raise exceptions.InvalidPersistenceStrategyError()
        if not persistence_strategy:
            # setup a default persistence strategy
            persistence_strategy = persistence_strategies \
                .DirectPersistenceStrategy(self.api)

        self.project_id = project_id
        self.persistence_strategy = persistence_strategy
        self.get_timeout = get_timeout
        self.post_timeout = post_timeout

    if sys.version_info[0] < 3:
        @staticmethod
        def check_project_id(project_id):

            ''' Python 2.x-compatible string typecheck. '''

            if not project_id or not isinstance(project_id, basestring):
                raise exceptions.InvalidProjectIdError(project_id)
    else:
        @staticmethod
        def check_project_id(project_id):

            ''' Python 3.x-compatible string typecheck. '''

            if not project_id or not isinstance(project_id, str):
                raise exceptions.InvalidProjectIdError(project_id)

    def add_event(self, event_collection, event_body, timestamp=None):
        """ Adds an event.

        Depending on the persistence strategy of the client,
        this will either result in the event being uploaded to Shushuo
        immediately or will result in saving the event to some local cache.

        :param event_collection: the name of the collection to insert the
        event to
        :param event_body: dict, the body of the event to insert the event to
        :param timestamp: datetime, optional, the timestamp of the event
        """
        event = Event(self.project_id, event_collection, event_body,
                      timestamp=timestamp)
        self.persistence_strategy.persist(event)

    def add_events(self, events):
        """ Adds a batch of events.

        Depending on the persistence strategy of the client,
        this will either result in the event being uploaded to Shushuo
        immediately or will result in saving the event to some local cache.

        :param events: dictionary of events
        """
        self.persistence_strategy.batch_persist(events)
