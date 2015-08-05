from peewee import *
from playhouse.db_url import connect, parse

from .findPackages import _caller_package
import inspect

# Custom error which fires if you try to use a database connection without explicelty opening it first
class DataBaseClosedError(DatabaseError): pass


def getDbConnection(db_object, callback, conn):
    '''
    Constructor for make_connection which is used to open a database connection
    and register a proper callback to lose the connection
    :param db_object:
    :param callback:
    :param conn:
    :return:
    '''

    def make_connection(request):
        '''
        1) open a database connection and return the database object for a registered database
        2) register a pyramid callback method to close the connection
        at the end if the request.
        :param request:
        :return:
        '''

        request.add_finished_callback(callback)
        print('opening connection for {}'.format(db_object))
        db_object.connect()
        return db_object
    return make_connection

def getcallback(db_object):
    '''
    constructor for pdb_finsied_callback, which is the callback method
    called at the end of a request used to close a database connection
    :param db_object:
    :return:
    '''

    def pdb_finished_callback(request):
        print('closing the connection for {}'.format(db_object))
        db_object.close()
    return pdb_finished_callback


def monkeyPatchDatabaseConnection(base):
    '''
    Monkey patching Database so that I get the desired
    error if you try to use the database
    without explicitly opening a connection,
    which is done by calling the proxy
    :param base:
    :return:

    '''
    def ok():
        print('ok')

    # Store the old get_conn method to use it later
    org_get_conn = base.get_conn

    # patch a new get_conn method which raises an error if the connection is closed
    # else it just calls the original get_conn method
    def get_conn():
        if base._Database__local.closed:
            raise DataBaseClosedError
        else:
            return org_get_conn()

    # apply monkey patch
    base.get_conn = get_conn
    base.ok = ok
    # add a database closed exception
    base.exceptions['DataBaseClosedError'] = DataBaseClosedError
    return base


def includeme(config):
    '''
    pyramid function which is called during application configuration to initilize this module
    :param config:
    :return:
    '''

    # print(_caller_package(('pyramid', 'pyramid.','pyramid_peewee','pyramid_peewee.')).__name__)
    # be sure our database modles are imported into your application configuration file
    mods = inspect.getmembers((_caller_package(('pyramid', 'pyramid.','pyramid_peewee','pyramid_peewee.'))))
    # print(mods[0][0])
    # get database connection urls from configuration
    db_urls = config.registry.settings['peewee.urls'].split()
    peewee_dbs = dict()
    peewee_db_conns = dict()
    for db_url in db_urls:
        peewee_db = parse(db_url)
        peewee_db['database_object'] = '{}'.format(peewee_db['database'].replace('.','_'))
        peewee_dbs[peewee_db['database_object']] = None
        conn = connect(db_url)
        peewee_db_conns[peewee_db['database_object']] = conn
        for m in mods:
            # find the imported database proxy module so what we can initilize it now
            if m[0] == peewee_db['database_object']:
                peewee_dbs[peewee_db['database_object']] = m[1]

        peewee_dbs[peewee_db['database_object']].initialize(conn)
        # ====
        # applying monkey patch
        # ====
        monkeyPatchedDatabase = monkeyPatchDatabaseConnection(peewee_dbs[peewee_db['database_object']].obj)
        peewee_dbs[peewee_db['database_object']].obj = monkeyPatchedDatabase
        # ===

    for pdb in peewee_dbs:
        # restister the database objects with the pyrmaid request
        locals()['{}_callback'.format(pdb)] = getcallback(peewee_dbs[pdb])
        locals()['{}'.format(pdb)] = getDbConnection(peewee_dbs[pdb],
                                                     locals()['{}_callback'.format(pdb)],
                                                     peewee_db_conns[pdb])
        config.add_request_method(locals()['{}'.format(pdb)],'{}'.format(pdb), reify=True)




