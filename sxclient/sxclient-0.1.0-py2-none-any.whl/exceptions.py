'''
Exceptions specific for the package.

Copyright (c) 2015 Skylable Ltd.
License: Apache 2.0, see LICENSE for more details.

'''

class SXClientException(Exception):
    '''
    General exception type for library-specific exceptions.
    '''


class InvalidAPIFunctionError(SXClientException):
    '''
    Should be raised when a given API function is invalid.
    '''


class InvalidOperationError(SXClientException):
    '''
    Should be raised when a given operation is invalid (i.e. absent from the
    'operations' module).
    '''


class InvalidUserKeyError(SXClientException):
    '''
    Should be raised when a user key is invalid.
    '''


class SXClusterError(SXClientException):
    '''
    Should be raised when a problem occurs during communication with the
    cluster.
    '''


class SXClusterFatalError(SXClusterError):
    '''
    Should be raised when the cluster communication problem is fatal.
    '''


class SXClusterNonFatalError(SXClusterError):
    '''
    Should be raised when the cluster communication problem is non-fatal.
    '''
