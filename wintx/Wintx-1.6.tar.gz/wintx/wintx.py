#!/usr/bin/python
"""MySQL Fabric wrapper for Wintx."""

# MySQL Connector Import
import mysql.connector
from mysql.connector import fabric
from mysql.connector import ProgrammingError
from mysql.connector import pooling

from mysql.connector import Error as MySQLError
from mysql.connector import IntegrityError
from mysql.connector import InterfaceError

import ConfigParser
import hashlib
import numpy as np
import os
import Queue
import sys
import time
import traceback

import matplotlib
# Set matplotlib to use png files instead of the native display screen.
matplotlib.use('Agg')
import pygrib

from datetime import datetime
from numpy import ma
from threading import Lock
from threading import Thread

class WintxError(Exception):
  """Base error class for Wintx errors"""
  pass

class WintxConfigError(WintxError):
  """Error class handling config errors"""
  pass

class WintxDatabaseError(WintxError):
  """Error class handling database errors"""
  pass

class Wintx(object):
  """WintxDatabase"""
  WINTX_COLLECTION_NAME = 'wintx_collection'

  QUERY_INSERT_LOCATION = 'INSERT `Location`(`lat_lon`) VALUES'
  QUERY_INSERT_LOCATION_VALUE = '(GeomFromText(\'POINT(%(latitude).20f %(longitude).20f)\'))'
  QUERY_INSERT_LEVEL =    'INSERT `Level`(`level`, `level_type`) VALUES'
  QUERY_INSERT_LEVEL_VALUE = '(%(level)d, \'%(leveltype)s\')'
  QUERY_INSERT_VARIABLE = 'INSERT `Variable`(`datatype`, `variable_name`) VALUES'
  QUERY_INSERT_VARIABLE_VALUE = '(\'%(datatype)s\', \'%(varname)s\')'
  QUERY_INSERT_DATA =     'INSERT INTO `Data`(`data_id`, `timestamp`, `loc_id`, `level_id`, `var_id`, `data`) VALUES'
  QUERY_INSERT_DATA_VALUE = '(UNHEX(\'%(data_id)s\'), %(timestamp)d, %(loc_id)d, %(level_id)d, %(var_id)d, %(value).20f)'

  QUERY_SELECT_LOCATION =  'SELECT `loc_id`, X(`lat_lon`), Y(`lat_lon`) FROM `Location`'
  QUERY_SELECT_LEVEL =     'SELECT `level_id`, `level`, `level_type` FROM `Level`'
  QUERY_SELECT_VARIABLE =  'SELECT `var_id`, `datatype`, `variable_name` FROM `Variable`'
  QUERY_SELECT_GTID_WAIT = 'SELECT WAIT_UNTIL_SQL_THREAD_AFTER_GTIDS(\'%s\', 0)'

  QUERY_SELECT_LOCATION_ID = 'SELECT `loc_id` FROM `Location` WHERE `lat_lon` = GeomFromText(\'POINT(%(latitude).20f %(longitude).20f)\')'
  QUERY_SELECT_LEVEL_ID =    'SELECT `level_id` FROM `Level` WHERE `level`=%(level)d AND `level_type` LIKE \'%(leveltype)s\''
  QUERY_SELECT_VARIABLE_ID = 'SELECT `var_id` FROM `Variable` WHERE `datatype` LIKE \'%(datatype)s\' AND `variable_name` LIKE \'%(varname)s\''

  QUERY_SELECT_DATA =     'SELECT Data.timestamp, X(Location.lat_lon), Y(Location.lat_lon), Level.level, ' \
      'Level.level_type, Variable.datatype, Variable.variable_name, Data.data FROM ' \
      'Data INNER JOIN Location ON Data.loc_id=Location.loc_id ' \
      'INNER JOIN Level ON Data.level_id=Level.level_id ' \
      'INNER JOIN Variable ON Data.var_id=Variable.var_id'

  CONFIG_FILE_SCHEME = {
      'mysql': {'db_name': 'str', 'user': 'str', 'password': 'str',
          'timeout': 'int', 'poolsize': 'int', 'bulkquantity': 'int', 'attempts': 'int'},
      'fabric': {'host': 'str', 'port': 'int', 'user': 'str',
          'password': 'str'},
      'groups': {'global': 'str', 'shards': 'list'}}

  def __init__(self, config_file='/etc/wintx.conf'):
    """Initializes a WintxDatabase object."""
    config_instance = ConfigParser.ConfigParser()
    # Read the config file
    if( not os.path.exists(config_file) ):
      raise WintxConfigError('Config file %s does not exist.' % config_file)
    files_read = config_instance.read([config_file])
    if( not files_read ):
      raise WintxConfigError('There was an error reading the config file %s.' % config_file)

    self.settings = {}

    for section in self.CONFIG_FILE_SCHEME:
      if( not config_instance.has_section(section) ):
        raise WintxConfigError('The config file does not have section %s.' % section)
      self.settings[section] = {}

      for option in self.CONFIG_FILE_SCHEME[section]:
        if( not config_instance.has_option(section, option) ):
          raise WintxConfigError('The config file does not have option %s in section %s.' % (option, section))

        if( self.CONFIG_FILE_SCHEME[section][option] == 'int' ):
          self.settings[section][option] = config_instance.getint(section, option)
        elif( self.CONFIG_FILE_SCHEME[section][option] == 'boolean' ):
          self.settings[section][option] = config_instance.getboolean(section, option)
        elif( self.CONFIG_FILE_SCHEME[section][option] == 'str' ):
          self.settings[section][option] = config_instance.get(section, option)
        elif( self.CONFIG_FILE_SCHEME[section][option] == 'list' ):
          self.settings[section][option] = config_instance.get(section, option).split(',')
        else:
          raise WintxConfigError('Option %s in section %s is an invalid type.' % (option, section, self.CONFIG_FILE_SCHEME[section][option]))

    self.db_name = self.settings['mysql']['db_name']
    self.shard_groups = self.settings['groups']['shards']
    self.global_group = self.settings['groups']['global']
    self.connection_attempts = self.settings['mysql']['attempts']
    self.db_config = {
        'fabric': {
          'username': self.settings['fabric']['user'],
          'password': self.settings['fabric']['password'],
          'host': self.settings['fabric']['host'],
          'port': self.settings['fabric']['port'],
        },
        'user': self.settings['mysql']['user'],
        'password': self.settings['mysql']['password'],
        'database': self.db_name,
        'connection_timeout': self.settings['mysql']['timeout'],
        #'ssl_ca': '',
        #'ssl_cert': '',
        #'ssl_key': '',
        'compress': False,
        'raise_on_warnings': False,
        'autocommit': True,
    }

    self.connection = None
    self.cursor = None

    # Small cache of metadata (location, variables, and levels) to help increase write speeds of grib file imports
    self.meta_locations = {}
    self.meta_variables = {}
    self.meta_levels = {}

    self.meta_lock = Lock()

    self.connect()

  def __del__(self):
    """Deconstructor to handle closing a persistent connection."""
    # Try to close the connection, but silently fail if connection has not
    # been initialized.
    try:
      if( self.connection is not None and self.isConnectedToServer() ):
        self.connection.disconnect()
    except Exception as err:
      pass

  def __setGlobalConnectionProperty__(self, connection=None, readonly=False):
    """Sets the properties of a connection for a global query."""
    if( connection is None ):
      connection = self.connection

    mode = fabric.MODE_READWRITE
    if( readonly ):
      mode = fabric.MODE_READONLY

    connection.set_property(
        mode=mode,
        scope=fabric.SCOPE_GLOBAL,
        group=self.global_group,
        tables=None,
        key=None,
    )

    self.connectDbServer(connection)

  def __setLocalConnectionProperty__(self, key, connection=None, readonly=False):
    """Sets the properties of a connection for a sharded query."""
    if( connection is None ):
      connection = self.connection

    mode = fabric.MODE_READWRITE
    if( readonly ):
      mode = fabric.MODE_READONLY

    connection.set_property(
        mode=mode,
        scope=fabric.SCOPE_LOCAL,
        group=None,
        tables=['%s.Data' % self.db_config['database']],
        key=key,
    )

    self.connectDbServer(connection)

  def __setLocalConnectionGroupProperty__(self, group, connection=None, readonly=False):
    """Sets the group property of a connection for a sharded query."""
    if( connection is None ):
      connection = self.connection

    mode = fabric.MODE_READWRITE
    if( readonly ):
      mode = fabric.MODE_READONLY

    connection.set_property(
        mode=mode,
        scope=fabric.SCOPE_LOCAL,
        group=group,
        tables=None,
        key=None,
    )

    self.connectDbServer(connection)

  def __getTimestamp__(self, time):
    """Converts a datetime into a timestamp."""
    #timestamp = (time - datetime.utcfromtimestamp(0)).total_seconds()
    dtime = (time - datetime.utcfromtimestamp(0))
    timestamp = (dtime.days * 86400) + dtime.seconds
    return int(timestamp)

  def __getTime__(self, timestamp):
    """Converts a timestamp into a datetime object."""
    time = datetime.utcfromtimestamp(timestamp)
    return time

  def connect(self):
    """Makes a connection to the MySQL Fabric server."""
    attempts = self.connection_attempts
    for i in range(1, attempts + 1):
      try:
        self.connection = mysql.connector.connect(**self.db_config)
        break
      except InterfaceError as err:
        if( i < attempts ):
          continue
        else:
          raise WintxDatabaseError('Was unable to form a stable connection to ' \
              '%s@%s:%s.' % (self.db_config['user'], self.db_config['host'],
                             self.db_config['port']))
      except MySQLError as e:
        raise WintxDatabaseError('Was unable to connect to %s@%s:%s - %s' %
            (self.db_config['user'], self.db_config['fabric']['host'], 
             self.db_config['fabric']['port'], str(e)))

    if( not self.isConnectedToServer ):
      raise WintxDatabaseError('Was unable to connect to %s@%s:%s for an unknown ' \
          'reason.' % (self.db_config['user'], self.db_config['host'], 
                       self.db_config['port']))

  def connectDbServer(self, connection):
    """Attempts to force MySQL Fabric to connect to the db server for the 
       group. This will attempt to connect n (default 3) times."""
    attempts = self.connection_attempts
    for i in range(1, attempts + 1):
      try:
        connection._connect()
        break
      except InterfaceError as err:
        if( i < attempts ):
          continue
        else:
          raise WintxDatabaseError('Failed to form underlying connection to ' \
              'database. MySQL Fabric reset the connection too many times.')

  def __safeFabricExecute__(self, fabric_command, args=[], kwargs={}):
    """TODO"""
    attempts = self.connection_attempts
    result = None

    for i in range(1, attempts + 1):
      try:
        result = fabric_command(*args, **kwargs)
        break
      except InterfaceError as err:
        if( i < attempts ):
          continue
        else:
          raise WintxDatabaseError('Was unable to form a stable connection to ' \
              '%s@%s:%s while executing command "%s".' % (self.db_config['user'],
              self.db_config['host'], self.db_config['port'], fabric_command.__name__))
      except Exception as err:
        raise err

    return result

  def isConnectedToServer(self):
    """Determine if a connection persists."""
    return self.connection is not None

  def __connectedOrDie__(self):
    """Checks if a connection is formed and raises an error if not."""
    if( not self.isConnectedToServer() ):
      raise WintxDatabaseError('Not connected to server.')
    return True

  def disconnect(self):
    """Ensures the global connection is closed."""
    if( self.cursor is not None ):
      self.cursor.close()
      self.cursor = None

    if( self.connection is not None or self.connection.is_connected ):
      self.connection.disconnect()
      self.connection = None

  def getWintxDict(self):
    """Returns dictionary of all wintx database columns."""
    return {'latitude': 0.0, 'longitude': 0.0, 'time': datetime.now(),
        'datatype': '', 'varname': '', 'leveltype': '', 'level': 0,
        'value': None}

  def getWintxIndexesDict(self):
    """Returns dictionary of all wintx indexed columns."""
    return {'latitude': 0.0, 'longitude': 0.0, 'vertical': 0, 'time': datetime.now(),
        'datatype': '', 'varname': '', 'level': 0, 'leveltype': ''}

  def __startTransaction__(self, snapshot=False, readonly=False):
    """Prepares a transaction and cursor for database operations. Limits to one
       global cursor at a time."""
    self.__connectedOrDie__()

    if( self.cursor is not None or self.connection.in_transaction ):
      raise WintxDatabaseError('A transaction is currently active. A new '\
          'transaction may not begin until the current transaction has completed.')

    try:
      self.connection.start_transaction(consistent_snapshot=snapshot, readonly=readonly)
      #self.cursor = self.connection.cursor(dictionary=True, buffered=False)

      self.cursor = self.connection.cursor()
    except ProgrammingError as e:
      if( self.cursor is not None ):
        self.cursor.close()

      if(self.connection.in_transaction ):
        self.connection.rollback()
      raise WintxDatabaseError('A transaction is currently active. A new '\
          'transaction may not begin until the current transaction has completed.')

  def __endTransaction__(self, commit=False):
    """Ends a transaction and closes the cursor."""
    self.__connectedOrDie__()

    if( self.cursor is not None ):
      try:
        for result in self.cursor:
          if( type(result) == type(()) ):
            break
          elif( result.with_rows ):
            result.fetchall()
        self.cursor.close()
      except Exception as err:
        raise WintxDatabaseError('Error closing the cursor: %s' % str(err))
    self.cursor = None

    if( self.connection.in_transaction ):
      if( commit ):
        self.connection.commit()
      else:
        self.connection.rollback()

  def checkQueryDict(self, query, restricted_columns=None):
    """Verifies a query dictionary is properly formed."""
    comparison_operands = ['<', '<=', '>', '>=', '==']

    if( query is None ):
      raise WintxDatabaseError('No query provided.')
    if( type(query) is not type({}) ):
      raise WintxDatabaseError('Query provided is not a dictionary.')

    if( restricted_columns is None ):
      restricted_columns = []
    elif( type(restricted_columns) is not type([]) and
          type(restricted_columns) is not type(()) ):
      raise WintxDatabaseError('Restricted column list provided is not a list or tuple.')

    for column in query:
      if( column in restricted_columns ):
        raise WintxDatabaseError('Column \'%s\' is not restricted for this query.' % column)
      if( column == 'latitude' or column == 'longitude' or column == 'level' ):
        if( type(query[column]) is not type(1) and
            type(query[column]) is not type(1.1) and
            type(query[column]) is not type({}) ):
          raise WintxDatabaseError('Query parameters provided for column \'%s\' is an invalid type.' % column)
        if( type(query[column]) is type({}) ):
          for comparison in query[column]:
            if( comparison not in comparison_operands ):
              raise WintxDatabaseError('Invalid comparison operation \'%s\' provided for column \'%s\'.' % (comparison, column))
            if( type(query[column][comparison]) is not type(1.1) and
                type(query[column][comparison]) is not type(1) ):
              raise WintxDatabaseError('Query parameter provided for comparison \'%s\' under column \'%s\' is an invalid type. Provided parameter type is \'%s\'' % (comparison, column, type(query[column][comparison])))
      elif( column == 'leveltype' or column == 'leveltype' or column == 'datatype' or column == 'varname' ):
        if( type(query[column]) is not type('') and
            type(query[column]) is not type(u'') and
            type(query[column]) is not type([]) ):
          raise WintxDatabaseError('Query parameters provided for column \'%s\' is an invalid type.' % column)
        if( type(query[column]) is type([]) ):
          for parameter in query[column]:
            if( type(parameter) is not type('') and
                type(parameter) is not type(u'') ):
              raise WintxDatabaseError('Invalid parameter type provided for column \'%s\'.' % column)
      elif( column == 'time' ):
        if( type(query[column]) is not type(datetime.now()) or type(query[column]) is not type({}) ):
          raise WintxDatabaseError('Query parameters provided for column \'%s\' is an invalid type.' % column)
        if( type(query[column]) is type({}) ):
          for comparison in query[column]:
            if( comparison not in comparison_operands ):
              raise WintxDatabaseError('Invalid comparison operation \'%s\' provided for column \'%s\'.' % (comparison, column))
            if( type(query[column][comparison]) is not type(datetime.now()) ):
              raise WintxDatabaseError('Query parameter provided for comparison \'%s\' under column \'%s\' is an invalid type.' % (comparison, column))
      else:
        raise WintxDatabaseError('unknown column \'%s\' found.' % column)

  def compareDictFromQuery(self, value, comparedict):
    """Checks the values of a comparison dictionary provided from a column in a query dictionary."""
    if( type(comparedict) is not type({}) ):
      return False

    result = True
    for comparison in comparedict:
      if( comparison == '<' ):
        result = result and (value < comparedict[comparison])
      elif( comparison == '<=' ):
        result = result and (value <= comparedict[comparison])
      elif( comparison == '>' ):
        result = result and (value > comparedict[comparison])
      elif( comparison == '>=' ):
        result = result and (value >= comparedict[comparison])
      elif( comparison == '==' ):
        result = result and (value == comparedict[comparison])
      else:
        raise WinxDatabaseError('Invalid comparison operation \'%s\' provided.' % comparison)
    return result

  def __checkRecordDict__(record):
    """Checks if supplied record is a properly formed Wintx dictionary."""
    if( not type(record) == type({}) ):
      raise WintxDatabaseError('Supplied record is not a dictionary.')

    wintx_dict = self.getWintxDict()
    for key in wintx_dict.getKeys():
      if( key not in record.getKeys() ):
        raise WintxDatabaseError('Supplied record dictionary missing key %s' % key)

  def __connectionThread__(self, thread_function, args, kwargs):
    """Creates a connection to be used by a given function."""
    thread_db_config = self.db_config.copy()
    del thread_db_config['connection_timeout']
    thread_db_config['autocommit'] = False
    thread_connection = mysql.connector.connect(**thread_db_config)
    thread_function(connection=thread_connection, *args, **kwargs)
    return

  def __multiThreadedConnections__(self, numTasks, thread_function, args, kwargs):
    """Executes a function across multiple threads, each with a unique connection."""
    threads = []

    numConnections = min(numTasks, self.settings['mysql']['poolsize'])
    if( numConnections > 1 ):
      for i in range(numConnections):
        threads.append(
            Thread(
                name='Wintx-Thread-%05d' % i,
                target=self.__connectionThread__,
                args=(thread_function, args, kwargs,),
        ))

      for thread in threads:
        thread.daemon = True
        thread.start()
      for thread in threads:
        thread.join()

    else:
      self.__connectionThread__(thread_function, args, kwargs)

    return

  def __prepareWhere__(self, query_dict, restricted=None):
    """Converts a dictionary query into a SQL where statement."""
    if( restricted is None ):
      restricted = []

    query = ''
    
    if( len(query_dict.keys()) > 0 ):
      query = "WHERE"

    first = True
    for key in query_dict:
      if( key in restricted ):
        raise WintxDatabaseError('Column "%s" is restricted for this query.' % key)

      column_name = ''
      column_eq = ''
      if( key=='time' ):
        column_name = 'Data.timestamp'
        column_eq = '='
      elif( key=='latitude' ):
        column_name = 'X(Location.lat_lon)'
        column_eq = '='
      elif( key=='longitude' ):
        column_name = 'Y(Location.lat_lon)'
        column_eq = '='
      elif( key=='level' ):
        column_name = 'Level.level'
        column_eq = '='
      elif( key=='leveltype' ):
        column_name = 'Level.level_type'
        column_eq = 'LIKE'
      elif( key=='datatype' ):
        column_name = 'Variable.datatype'
        column_eq = 'LIKE'
      elif( key=='varname' ):
        column_name = 'Variable.variable_name'
        column_eq = 'LIKE'
      else:
        raise WintxDatabaseError('Invalid column name found in query. '\
            'Column "%s" does not exist.' % key)

      if( type(query_dict[key]) == type({}) ):
        for param in query_dict[key]:
          comparison = ''
          if( param=='>' ):
            comparison = '>'
          if( param=='>=' ):
            comparison = '>='
          elif( param=='<' ):
            comparison = '<'
          elif( param=='<=' ):
            comparison = '<='
          elif( param=='==' ):
            comparison = column_eq

          value = query_dict[key][param]
          if( key=='time' ):
            value = self.__getTimestamp__(value)

          if( first ):
            first = False
          else:
            query = "%s AND" % query

          if( comparison=='LIKE' ):
            value = '"%s"' % value
          query = "%s %s %s %s" % (query, column_name, comparison, value)
      else:
        value = query_dict[key]
        if( key=='time' ):
          value = self.__getTimestamp__(value)

        if( first ):
          first = False
        else:
          query = "%s AND" % query

        if( column_eq=='LIKE' ):
          value = '"%s"' % value
        query = "%s %s %s %s" % (query, column_name, column_eq, value)

    return query

  def __queryAllShardsThread__(self, groupQueue, query, resultList, connection=None):
    """Thread instance handling querying individual shard groups."""
    connection.set_property(scope=fabric.SCOPE_LOCAL, mode=fabric.MODE_READONLY)

    while( not groupQueue.empty() ):
      group = groupQueue.get()
      connection.set_property(group=group)

      cursor = connection.cursor()
      cursor.execute(query)
      results = cursor.fetchall()
      cursor.close()

      self.meta_lock.acquire()
      for result in results:
        resultList.append(result)
      self.meta_lock.release()

      groupQueue.task_done()

  def __queryAllShards__(self, query):
    """Executes a query across all shard groups."""
    results = []
    groupQueue = Queue.Queue()
    for group in self.shard_groups:
      groupQueue.put(group)

    self.__multiThreadedConnections__(groupQueue.qsize(), self.__queryAllShardsThread__, (groupQueue, query, results), {})
    return results

  def __finalizeRecords__(self, results, sort=None):
    """Prepares results from a query into a list of dictionary entries, sorted if specified."""
    records = []
    for record in results:
      records.append({'time': self.__getTime__(record[0]), 'latitude': record[1],
          'longitude': record[2], 'level': record[3], 'leveltype': record[4],
          'datatype': record[5], 'varname': record[6], 'value': record[7]})
   
    if( sort is not None ):
      if( type(sort) is not type([]) ):
        raise WintxDatabaseError('Sort parameters should be given as a list.')

      sort.reverse()
      for column in sort:
        if( column[1].lower() == 'asc' ):
          records.sort(key=lambda item: item[column[0]], reverse=False)
        elif( column[1].lower() == 'dsc' ):
          records.sort(key=lambda item: item[column[0]], reverse=True)
        else:
          raise WintxDatabaseError('Invalid sort direction \'%s\'' % column[1])

    return records

  def query(self, query_dict, sort_column=None):
    """Queries the database for records in a readonly environment.
    Inputs:
      query_dict: dictionary forming a query request
      sort_column: column, direction tuple list in order of complex sort
        example: [('time', 'asc'), ('leveltype', 'asc'), ('level', 'dsc')]
    Outputs:
      list: of finalized record dictionaries
    """
    
    self.__connectedOrDie__()

    query = '%s' % self.QUERY_SELECT_DATA
    where_clause = self.__prepareWhere__(query_dict)
    query = "%s %s" % (query, where_clause)

    results = self.__queryAllShards__(query)
    records = self.__finalizeRecords__(results, sort_column)

    return records

  def queryWithin(self, polygon, query_dict, reverse_points=False, sort_column=None):
    """A spatial query finding all points within a polygon.
    Inputs:
      polygon: point tuple list ordered by sequence of points forming a shape
        example: [(1, 1), (1, 2), (2, 2), (2, 1)]
      query_dict: dictionary forming a query request
      reverse_points: boolean specifying if each point tuple needs to be flipped
        example: if true and given point (1, 2), point will be read as (2, 1)
      sort_column: column, direction tuple list in order of complex sort
        example: [('time', 'asc'), ('leveltype', 'asc'), ('level', 'dsc')]
    Outputs:
      list: of finalized record dictionaries
    """
    restricted_columns = ['latitude', 'longitude']

    query = '%s' % self.QUERY_SELECT_DATA
    where_clause = self.__prepareWhere__(query_dict, restricted=restricted_columns)

    first_point = polygon[0]
    poly_where = 'CONTAINS(GeomFromText("POLYGON(('

    if( reverse_points ):
      for point in polygon:
        poly_where = '%s%.20f %.20f, ' % (poly_where, point[1], point[0])
      poly_where = '%s%.20f %.20f))"), `lat_lon`)' % (poly_where, first_point[1], first_point[0])
    else:
      for point in polygon:
        poly_where = '%s%.20f %.20f, ' % (poly_where, point[0], point[1])
      poly_where = '%s%.20f %.20f))"), `lat_lon`)' % (poly_where, first_point[0], first_point[1])

    if( where_clause == '' ):
      query = '%s WHERE %s' % (query, poly_where)
    else:
      query = '%s %s AND %s' % (query, where_clause, poly_where)

    results = self.__queryAllShards__(query)
    records = self.__finalizeRecords__(results, sort_column)
    return records

  def __getOrAddId__(self, cache, key, find_query, insert_query):
    """Find or insert metadata.
    Searches the cache, then the database for a metadata id. If the metadata
    does not exist, insert the metadata into the database.
    Inputs:
      cache: dictionary of the metadata
      key: tuple of the metadata forming the metadata key
        example: (latitude, longitude) or (level, leveltype)
      find_query: database query to search for metadata
      insert_query: database query to insert metadata
    Outputs:
      int: database id of metadata
    """
    key_id = -1

    if( not cache.has_key(key) ):
      self.__setGlobalConnectionProperty__()
      self.__startTransaction__()
      commit = True
      gtid_sync = None
      results = None

      try:
        self.cursor.execute(find_query)
        results = self.cursor.fetchall()
      except MySQLError as err:
        results = []

      if( not results ):
        try:
          self.cursor.execute(insert_query)
          key_id = self.cursor.lastrowid

          self.cursor.execute("SELECT @@global.gtid_executed")
          gtid_sync = self.cursor.fetchall()[0][0]
        except MySQLError as err:
          commit = False
          raise WintxDatabaseError('Failed to insert metadata key %s.' % key)
      else:
        key_id = results[0][0]

      self.__endTransaction__(commit)

      cache[key] = (key_id, gtid_sync)
    else:
      key_id = cache[key][0]

    return key_id

  def __setBulkMeta__(self, cache, records):
    """Places records into the cache.
    Inputs:
      cache: metadata dictionary for records to cache within
      records: record metadata to be cached
    """
    for r in records:
      cache[(r[1], r[2])] = (r[0], None)

  def clearMetadataCache(self):
    """Clears the local metadata cache."""
    del self.meta_locations
    del self.meta_levels
    del self.meta_variables
    self.meta_locations = {}
    self.meta_levels = {}
    self.meta_variables = {}

  def loadMetadataCache(self):
    """Loads the metadata into a local cache."""
    if( not self.meta_levels or not self.meta_variables or not self.meta_locations ):
      self.meta_levels = {}
      self.meta_locations = {}
      self.meta_variables = {}

      self.__setGlobalConnectionProperty__(readonly=True)
      self.__startTransaction__(readonly=True)

      self.cursor.execute(self.QUERY_SELECT_LOCATION)
      self.__setBulkMeta__(self.meta_locations, self.cursor.fetchall())
      self.cursor.execute(self.QUERY_SELECT_LEVEL)
      self.__setBulkMeta__(self.meta_levels, self.cursor.fetchall())
      self.cursor.execute(self.QUERY_SELECT_VARIABLE)
      self.__setBulkMeta__(self.meta_variables, self.cursor.fetchall())

      self.__endTransaction__()

  def __formDataDict__(self, record):
    """Forms insert ready dictionary.
    It is assumed that the cache has been loaded prior this call.
    Inputs:
      record: dictionary containing a data point's metadata and data values
    Outputs:
      dictionary: insert ready dictionary containing metadata id's and data values
        format: {'loc_id': 1, 'var_id': 1, 'level_id': 1,
                 'timestamp': datetime, 'value': 1.0}
    """
    loc_id = self.meta_locations[record['latitude'], record['longitude']][0]
    level_id = self.meta_levels[record['level'], record['leveltype']][0]
    var_id = self.meta_variables[record['datatype'], record['varname']][0]
    timestamp = self.__getTimestamp__(record['time'])

    data_dict = {'timestamp': timestamp, 'data_id': None,
        'value': record['value'], 'loc_id': loc_id,
        'var_id': var_id,
        'level_id': level_id}

    data_dict['data_id'] = hashlib.md5('%(timestamp)d-%(loc_id)s-%(level_id)s-%(var_id)s' % data_dict).hexdigest()

    return data_dict

  def __determineShardGroup__(self, data_dict):
    """Retreives the shard group that MySQL Fabric determines the record belongs to.
    Inputs:
      data_dict: a dictionary prepared to be inserted into the Data table
    Outputs:
      string: name of the shard group the record will insert into
    """
    key = data_dict['data_id']
    table = '%s.Data' % self.db_name
    server = self.__safeFabricExecute__(self.connection._fabric.get_shard_server,
        [(table,), key], {'scope': fabric.SCOPE_LOCAL, 'mode': fabric.MODE_READWRITE})
    return server[1]

  def __makeRecordGroupJobQueue__(self, groups_dict):
    """Converts a dictionary of group to record lists into list of jobs.
    This will split record lists into multiple lists with 
    bulkquantity records per list.
    Inputs:
      groups_dict: dictionary of record lists keyed by group names.
    Outputs:
      Queue: of job dictionaries containing group information and a record list
             with no more than bulkquantity records
    """
    jobs_count = 0
    jobList = {}
    jobQueue = Queue.Queue()
    record_import_quantity = self.settings['mysql']['bulkquantity']

    for group in groups_dict:
      count = 0
      cur_list = []
      jobList[group] = []
      jobList[group].append(cur_list)

      for data_dict in groups_dict[group]:
        count = count + 1
        if( count % record_import_quantity == 0 ):
          cur_list = []
          jobList[group].append(cur_list)
        cur_list.append(data_dict)
      jobs_count = jobs_count + len(jobList[group])

    # Distributes jobs so groups evenly receive thread time
    while( jobQueue.qsize() < jobs_count ):
      for group in jobList:
        try:
          job = jobList[group].pop()
          jobQueue.put({'group': group, 'records': job})
        except IndexError as err:
          pass

    return jobQueue

  def __threadMetadataInsert__(self, metadataQueue, connection=None):
    """Inserts metadata in bulk."""
    while ( not metadataQueue.empty() ):
      try:
        job = metadataQueue.get(block=False)
      except Queue.Empty as err:
        continue

      group = job['group']
      records = job['records']
      if( len(records) == 0 ):
        continue

      query = ''
      value = ''
      if( group == 'global_loc' ):
        query = self.QUERY_INSERT_LOCATION
        value = self.QUERY_INSERT_LOCATION_VALUE
      elif( group == 'global_var' ):
        query = self.QUERY_INSERT_VARIABLE
        value = self.QUERY_INSERT_VARIABLE_VALUE
      elif( group == 'global_lev' ):
        query = self.QUERY_INSERT_LEVEL
        value = self.QUERY_INSERT_LEVEL_VALUE
      else:
        raise WintxDatabaseError('Invalid group provided for metadata import. Group: %s' % group)

      self.__setGlobalConnectionProperty__(connection=connection)

      cursor = None
      attempt = 0
      while( cursor is None ):
        attempt = attempt + 1
        if( attempt > 6 ):
          raise WintxDatabaseError('Failed to connect to fabric global server.')
        try:
          cursor = connection.cursor()
        except InterfaceError as err:
          cursor = None
          continue

      importBatch = []
      for rec in records:
        importBatch.append(value % rec)
      cursor.execute('%s %s' % (query, ', '.join(importBatch)))

      cursor.close()
      cursor = None
      connection.commit()
      metadataQueue.task_done()

    return

  def __insertRecord__(self, record, insert_dict, cursor):
    """Inserts record into the server of a given cursor.
    Inputs:
      record: dicitionary containing metadata and data values for data point
      insert_dict: insert ready data dictionary
      cursor: a connected Fabric cursor with local/global properties set
    """
    try:
      cursor.execute(self.QUERY_INSERT_DATA % insert_dict)
    except IntegrityError as err:
      # Foreign Key Failure
      if( err.errno == 1452 ):
        if( 'Location' in str(err) ):
          loc_id = (record['latitude'], record['longitude'])
          if( self.meta_locations[loc_id][1] is None ):
            raise WintxDatabaseError('Foreign key constraint error with "Location" table. GTID sync key not found. The location metadata was not successfully inserted.')
          gtid = self.meta_locations[loc_id][1]
          cursor.execute(self.QUERY_SELECT_GTID_WAIT % gtid)
          cursor.fetchall()
        elif( 'Variable' in str(err) ):
          var_id = (record['datatype'], record['varname'])
          if( self.meta_variables[var_id][1] is None ):
            raise WintxDatabaseError('Foreign key constraint error with "Variable" table. GTID sync key not found. The variable metadata was not successfully inserted.')
          gtid = self.meta_variables[var_id][1]
          cursor.execute(self.QUERY_SELECT_GTID_WAIT % gtid)
          cursor.fetchall()
        elif( 'Level' in str(err) ):
          level_id = (record['level'], record['leveltype'])
          if( self.meta_levels[level_id][1] ):
            raise WintxDatabaseError('Foreign key constraint error with "Level" table. GTID sync key not found. The level metadata was not successfully inserted.')
          gtid = self.meta_levels[level_id][1]
          cursor.execute(self.QUERY_SELECT_GTID_WAIT % gtid)
          cursor.fetchall()
        else:
          raise WintxDatabaseError('Unknown foreign key constraint error: %s' % str(err))

        self.__insertRecord__(record, insert_dict, cursor)

      # Duplicate Key
      elif( err.errno == 1022 ):
        raise WintxDatabaseError('Duplicate record found for %s.' % record)
    except MySQLError as err:
      raise WintxDatabaseError('unknown database error occurred: %s' % str(err))

  def __threadInsert__(self, jobQueue, resultDict, connection=None):
    """Thread instance handling inserting a data record."""
    successful_records = 0
    duplicate_records = []
    errors_list = []

    while( not jobQueue.empty() ):
      try:
        job = jobQueue.get(block=False)
      except Queue.Empty as err:
        continue
      shard_group = job['group']
      records = job['records']

      self.__setLocalConnectionGroupProperty__(shard_group, connection=connection)
      connection.start_transaction(readonly=False)
      cursor = None

      # Connections were not connecting, had to run multiple times to successfully  connect
      attempt = 0
      while( cursor is None ):
        attempt = attempt + 1
        if( attempt > 6 ):
          raise WintxDatabaseError('Failed to connect to fabric server for group %s.' % shard_group)
        try:
          cursor = connection.cursor()
        except InterfaceError as err:
          cursor = None
          pass

      importData = []
      data_ids = []
      data_id_mapping = {}
      for rec in records:
        data_ids.append('UNHEX(\'%s\')' % rec[1]['data_id'])
        data_id_mapping[rec[1]['data_id']] = rec[0]
      
      # Check for duplicate ids
      cursor.execute('SELECT HEX(`data_id`) FROM `Data` WHERE `data_id` IN (%s)' % ', '.join(data_ids))
      results = cursor.fetchall()
      if( len(results) > 0 ):
        for res in results:
          if( res[0].lower() in data_id_mapping.keys() ):
            duplicate_records.append(data_id_mapping[res[0].lower()])

      for rec in records:
        if( rec[0] not in duplicate_records ):
          importData.append(self.QUERY_INSERT_DATA_VALUE % rec[1])

      if( len(importData) > 0 ):
        try:
          cursor.execute('SET foreign_key_checks=0')
          cursor.execute('SET unique_checks=0')
          cursor.execute('%s %s' % (self.QUERY_INSERT_DATA, ', '.join(importData)))
          cursor.execute('SET unique_checks=1')
          cursor.execute('SET foreign_key_checks=1')
          successful_records = successful_records+ len(importData)
        except IntegrityError as err:
          errors_list.append(str(err))
        except MySQLError as err:
          errors_list.append(str(err))

      cursor.close()
      cursor = None

      connection.commit()

      jobQueue.task_done()

    self.meta_lock.acquire()
    resultDict['insertedRecords'] = resultDict['insertedRecords'] + successful_records
    resultDict['duplicateRecords'] = resultDict['duplicateRecords'] + duplicate_records
    resultDict['errors'] = resultDict['errors'] + errors_list
    self.meta_lock.release()
    return

  def insertBulk(self, records, clear_cache=False):
    """Inserts multiple records."""
    self.__connectedOrDie__()

    self.loadMetadataCache()

    results = {
        'insertedRecords': 0,
        'duplicateRecords': [],
        'errors': []
    }

    insert_loc = set()
    insert_var = set()
    insert_lev = set()

    # Prepare metadata for import
    for record in records:
      loc = (record['latitude'], record['longitude'])
      var = (record['datatype'], record['varname'])
      lev = (record['level'], record['leveltype'])
      if( not self.meta_locations.has_key(loc) ):
        insert_loc.add(loc)
      if( not self.meta_variables.has_key(var) ):
        insert_var.add(var)
      if( not self.meta_levels.has_key(lev) ):
        insert_lev.add(lev)

    # Import metadata
    metadataList = {'global_loc': [],
        'global_lev': [],
        'global_var': []}
    if( len(insert_loc) > 0 ):
      for loc in insert_loc:
        metadataList['global_loc'].append({'latitude': loc[0], 'longitude': loc[1]})
    if( len(insert_lev) > 0 ):
      for lev in insert_lev:
        metadataList['global_lev'].append({'level': lev[0], 'leveltype': lev[1]})
    if( len(insert_var) > 0 ):
      for var in insert_var:
        metadataList['global_var'].append({'datatype': var[0], 'varname': var[1]})
    metadataQueue = self.__makeRecordGroupJobQueue__(metadataList)
    self.__multiThreadedConnections__(metadataQueue.qsize(), self.__threadMetadataInsert__, (metadataQueue,), {})

    self.clearMetadataCache()
    self.loadMetadataCache()

    # Sorts records into their shard groups
    shard_groups = {}
    for record in records:
      data_dict = self.__formDataDict__(record)
      shard = self.__determineShardGroup__(data_dict)
      if( shard not in shard_groups ):
        shard_groups[shard] = []
      shard_groups[shard].append((record, data_dict))

    jobQueue = self.__makeRecordGroupJobQueue__(shard_groups)

    # Create the threads handling record imports
    self.__multiThreadedConnections__(jobQueue.qsize(), self.__threadInsert__, (jobQueue, results), {})

    if( clear_cache ):
      self.clearMetadataCache()

    return results

  def __checkDictForPass__(self, value, dictvalue):
    """Checks a query dictionary's dictionary value against a value to determine
       if the importer should pass on this set of records."""
    if( dictvalue is not None and
        not (type(dictvalue) is not type({}) and dictvalue == value) and
        not self.compareDictFromQuery(value, dictvalue) ):
      return True
    return False

  def __checkListForPass__(self, value, listvalue):
    """Checks a query dictionary's list value against a value to determine
       if the importer should pass on this set of records."""
    if( listvalue is not None and
        not ((type(listvalue) is type([]) or type(listvalue) is type((1,)))
             and value in listvalue) and
        listvalue != value ):
      return True
    return False

  def importGrib(self, gribFile, datatype, parameters=None, ignore_unknowns=False, longitude_convert_east=False):
    """Imports records from a GRIB2 file."""
    if( not os.path.exists(gribFile) ):
      raise WintxError('Grib file \'%s\' does not exist.' % gribFile)

    results = {'insertedRecords': 0, 'duplicateRecords': [], 'errors': []}

    restrict_time = None
    restrict_latitude = None
    restrict_longitude = None
    restrict_varname = None
    restrict_level = None
    restrict_leveltype = None

    if( parameters is not None ):
      self.checkQueryDict(parameters, ['datatype', 'time'])
      for column in parameters:
        if( column == 'time' ):
          restrict_time = parameters[column]
        elif( column == 'latitude' ):
          restrict_latitude = parameters[column]
        elif( column == 'longitude' ):
          restrict_longitude = parameters[column]
        elif( column == 'varname' ):
          restrict_varname = parameters[column]
        elif( column == 'level' ):
          restrict_level = parameters[column]
        elif( column == 'leveltype' ):
          restrict_leveltype = parameters[column]

    wintx_input_dict = self.getWintxDict()
    wintx_input_dict['datatype'] = datatype

    gribs_handle = pygrib.open(gribFile)

    docs_to_insert = []
    for grib in gribs_handle:
      wintx_input_dict['time'] = grib.analDate
      wintx_input_dict['varname'] = grib['name']
      wintx_input_dict['level'] = grib['level']
      wintx_input_dict['leveltype'] = grib['typeOfLevel']

      if( wintx_input_dict['leveltype'].lower() == 'unknown' ):
        if( ignore_unknowns ):
          continue
        else:
          raise WintxError('Unknown level type found. Fixed surface: %s' % grib['typeOfFirstFixedSurface'])

      if( wintx_input_dict['varname'].lower() == 'unknown' ):
        if( ignore_unknowns ):
          continue
        else:
          raise WintxError('Unknown variable name found. Fixed surface: %s' % grib['typeOfFirstFixedSurface'])
      
      if( self.__checkDictForPass__(wintx_input_dict['time'], restrict_time) ):
        continue
      if( self.__checkListForPass__(wintx_input_dict['varname'], restrict_varname) ):
        continue
      if( self.__checkDictForPass__(wintx_input_dict['level'], restrict_level) ):
        continue
      if( self.__checkListForPass__(wintx_input_dict['leveltype'], restrict_leveltype) ):
        continue

      lat_lons = grib.latlons()
      latitudes = lat_lons[0]
      longitudes = lat_lons[1]
      values = grib.values

      for loc_i in range(0, len(latitudes)):
        for loc_j in range(0, len(latitudes[loc_i])):
          # Check that the value in numpy masked array is not masked. If masked, don't add.
          if( values[loc_i][loc_j] is not ma.masked ):
            wintx_input_dict['latitude'] = np.asscalar(np.float32(latitudes[loc_i][loc_j]))
            wintx_input_dict['longitude'] = np.asscalar(np.float32(longitudes[loc_i][loc_j]))
            if( longitude_convert_east and wintx_input_dict['longitude'] > 180.0 ):
              wintx_input_dict['longitude'] = wintx_input_dict['longitude'] - 360.0

            wintx_input_dict['value'] = np.asscalar(np.float64(values[loc_i][loc_j]))

            if( self.__checkDictForPass__(wintx_input_dict['latitude'], restrict_latitude) ):
              continue
            if( self.__checkDictForPass__(wintx_input_dict['longitude'], restrict_longitude) ):
              continue

            docs_to_insert.append(wintx_input_dict.copy())

    res = self.insertBulk(docs_to_insert)
    results['insertedRecords'] = results['insertedRecords'] + res['insertedRecords']
    results['duplicateRecords'] = results['duplicateRecords'] + res['duplicateRecords']
    results['errors'] = results['errors'] + res['errors']

    gribs_handle.close()

    return results 

  def getTimes(self):
    """Retreives the unique timestamps stored in the database."""
    self.__connectedOrDie__()
    results = self.__queryAllShards__("SELECT DISTINCT(`timestamp`) FROM Data")

    timestamps = set()
    for timestamp in results:
      timestamps.add(timestamp[0])

    final_times = []
    for timestamp in timestamps:
      final_times.append(self.__getTime__(timestamp))

    final_times.sort()
    return final_times

  def getVariables(self):
    """Retreives the variables stored in the database."""
    self.__connectedOrDie__()
    self.__setGlobalConnectionProperty__()
    self.__startTransaction__(readonly=True)
    self.cursor.execute('SELECT DISTINCT(`variable_name`) FROM `Variable` ORDER BY `variable_name` ASC')
    results = self.cursor.fetchall()
    self.__endTransaction__()

    variables = []
    for r in results:
      variables.append(r[0])

    return variables

  def getLevels(self):
    """Retreives the levels stored in the database."""
    self.__connectedOrDie__()
    self.__setGlobalConnectionProperty__()
    self.__startTransaction__(readonly=True)
    self.cursor.execute('SELECT `level`, `level_type` FROM `Level` ORDER BY `level_type`, `level` ASC')
    results = self.cursor.fetchall()
    self.__endTransaction__()

    levels = []
    for r in results:
      levels.append((r[1], r[0]))

    return levels

  def getLocationCorners(self):
    """Retreives the corners of the stored latitude/longitude values in the database."""
    self.__connectedOrDie__()
    self.__setGlobalConnectionProperty__()
    self.__startTransaction__(readonly=True)
    self.cursor.execute('SELECT MAX(X(`lat_lon`)) AS `MAX_LAT`, ' \
        'MIN(X(`lat_lon`)) AS `MIN_LAT`, MAX(Y(`lat_lon`)) AS `MAX_LON`, ' \
        'MAX(Y(`lat_lon`)) AS `MIN_LON` FROM `Location`')
    results = self.cursor.fetchall()
    self.__endTransaction__()

    lat_max = results[0][0]
    lat_min = results[0][1]
    lon_max = results[0][2]
    lon_min = results[0][3]

    corners = {
        'topright':    (lat_max, lon_max),
        'topleft':     (lat_max, lon_min),
        'bottomright': (lat_min, lon_max),
        'bottomleft':  (lat_min, lon_min),
    }

    return corners

  def getDatabaseStats(self):
    """Retreives the size of the database and tables.
       Return: dict
    """
    self.__connectedOrDie__()
    stat_dict = {
        'totalSize': 0,
        'numRecords': 0,
        'avgRecordSize': 0,
        'numIndexes': 0,
        'indexSize': 0,
        'indexes': []}

    stats = {
        'database': stat_dict.copy(),
        'tables': {}}

    tables = self.__queryAllShards__('SHOW TABLE STATUS FROM %s' % self.settings['mysql']['db_name'])

    for table in tables:
      if( table[0] == u'Data' ):
        stats['database']['numRecords'] = table[4]
        stats['database']['avgRecordSize'] = table[5]
      stats['database']['totalSize'] = stats['database']['totalSize'] + table[6]
      stats['database']['indexSize'] = stats['database']['indexSize'] + table[8]
      stats['tables'][table[0]] = stat_dict.copy()
      stats['tables'][table[0]]['totalSize'] = table[6]
      stats['tables'][table[0]]['numRecords'] = table[4]
      stats['tables'][table[0]]['avgRecordSize'] = table[5]
      stats['tables'][table[0]]['indexSize'] = table[8]

    return stats
