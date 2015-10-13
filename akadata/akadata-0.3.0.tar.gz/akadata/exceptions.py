# Copyright (c) 2015, RedJack, LLC.
# All rights reserved.
#
# Please see the COPYING file in this distribution for license details.


class EdgeScapeException(Exception):
    """
    Base class for EdgeScape exceptions.

    Subclasses should provide `.status_code` and `detail` properties.
    """

    def __init__(self, status_code, detail=None):
        self.status_code = status_code
        self.detail = detail or self.default_detail

    def __str__(self):
        return self.detail

    @property
    def default_detail(self):
        return 'Invalid response with status code %d.' % self.status_code


class InvalidVersion(EdgeScapeException):

    def __init__(self, status_code, query_version, result_version):
        self.status_code = status_code
        self.query_version = query_version
        self.result_version = result_version

    @property
    def detail(self):
        return 'Expected version {}, received version {}.'.format(
            self.query_version, self.result_version)


class InvalidAddress(EdgeScapeException):

    def __init__(self, status_code, query_address, result_address):
        self.status_code = status_code
        self.query_address = query_address
        self.result_address = result_address

    @property
    def detail(self):
        return 'Queried address {}, received response for address {}.'.format(
            self.query_address, self.result_address)
