# -*- coding: utf-8-*-
# ###################################################################
# FILENAME: twisted_cql/session.py
# PROJECT: 
# DESCRIPTION: Cassandra session wrappers.
#
# ###################################################################
# (C)2015 DigiTar, All Rights Reserved
# ###################################################################

import cassandra.cluster
import cassandra.auth
import cassandra.query
from cassandra import AuthenticationFailed
from cassandra import ConsistencyLevel

from twisted.internet import threads
from twisted.internet import defer

class CassandraSession(object):
    """
    Thin wrapper around Datastax's cassandra-driver for Python.
    """
    
    def __init__(self, hosts, port=9042, keyspace=None, username=None, password=None, authenticator=cassandra.auth.PlainTextAuthProvider, protocol_version=3):
        """
        Initialize a new cassandra Session object to run queries against.
        
        Arguments:
            hosts (list) - List of strings of IPs/hostnames forming known Cassandra 
                           cluster servers.
            port (int) (default: 9042) 
                - TCP port to use when connecting to cluster.
            keyspace (unicode) (optional) - Default keyspace to use.
            authenticator (cassandra.auth.AuthProvider) (default: cassandra.auth.PlainTextAuthProvider) 
                - Authentication provider to use when authenticating.
            username (unicode) (default: None)- Username to use when connecting to cluster.
            password (unicode) (default: None) - Password to use when connecting to cluster.
            protocol_version (int) (default: 3) - Cassandra protocol version to use.
        Returns:
            Success: returns CassandraSession instance.
            Failure: Raises exception.
        """
        
        self.hosts = hosts
        self.port = port
        self._keyspace = keyspace
        
        self._set_auth(username=username,password=password,authenticator=authenticator)
        self._cluster = cassandra.cluster.Cluster(self.hosts,self.port,auth_provider=self._auth_provider,protocol_version=protocol_version)
        self._session = None
        
    def _set_auth(self, username=None, password=None, authenticator=cassandra.auth.PlainTextAuthProvider):
        """
        Set authentication parameters.
        """
        if username != None and password != None:
            self._auth_provider = authenticator(username=username,password=password)
        else:
            self._auth_provider = None
    
    @defer.inlineCallbacks
    def connect(self, keyspace=None):
        """
        Initiate connection to cluster.
        
        Arguments:
            keyspace (str) (optional) - Keyspace to use.
        
        Returns:
            Success: True (via Deferred)
            Failure: Raises exception.
        """
        
        if keyspace:
            self._keyspace = keyspace
        
        try:
            self._session = yield threads.deferToThread(self._cluster.connect, keyspace=self._keyspace)
        except cassandra.cluster.NoHostAvailable, e:
            for host_key in e.args[1].keys():
                if isinstance(e.args[1][host_key], cassandra.AuthenticationFailed):
                    raise e.args[1][host_key]
                else:
                    print "%s: Unexpected Error - %s" % (host_key, repr(e.args[1][host_key]))
                    raise e
        
        defer.returnValue(True)
    
    @defer.inlineCallbacks
    def execute(self, *args, **kwargs):
        """
        Deferred wrapper for cassandra.cluster.Session.execute.
        
        Returns:
            Success: list of rows (via Deferred)
            Failure: Raises exception.
        """
        
        if not self._session:
            yield self.connect()
        
        rows = yield threads.deferToThread(self._session.execute, *args, **kwargs)
        
        defer.returnValue(rows)
    
    def execute_query(self, query, query_args=None, consistency_level=ConsistencyLevel.ONE):
        """
        Run CQL query with optional query arguments and specified consistency_level.
        
        Arguments:
            query (unicode) - CQL query string (with format specifiers if needed).
            query_args (list,tuple,dict) (optional) - Argument(s) for query.
            consistency_level (int enum) - Consistency level specified by cassandra.ConsistencyLevel
                                           enum member.
        
        Returns:
            Success: list of rows (via Deferred)
            Failure: Raises exception.
        """
        
        query_obj = cassandra.query.SimpleStatement(query,consistency_level=consistency_level)
        return self.execute(query_obj,query_args)
        