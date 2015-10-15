# coding: utf-8

# Copyright (c) 2015, thumbor-community
# Use of this source code is governed by the MIT license that can be
# found in the LICENSE file.

import botocore.session

from tornado_botocore import Botocore
from tornado.concurrent import return_future

class Bucket(object):
    """
    This handles all communication with AWS API
    """
    _bucket      = None
    _region      = None
    _local_cache = dict()

    def __init__(self, bucket, region):
        """
        Constructor
        :param string bucket: The bucket name
        :param string region: The AWS API region to use
        :return: The created bucket
        """
        self._bucket = bucket
        self._region = region

    @return_future
    def get(self, path, callback=None):
        """
        Returns object at given path
        :param string path: Path or 'key' to retrieve AWS object
        :param callable callback: Callback function for once the retrieval is done
        """
        session = Botocore(service='s3', region_name=self._region, operation='GetObject')
        session.call(
            callback=callback,
            Bucket=self._bucket,
            Key=path,
        )

    @return_future
    def get_url(self, path, method='GET', expiry=3600, callback=None):
        """
        Generates the presigned url for given key & methods
        :param string path: Path or 'key' for requested object
        :param string method: Method for requested URL
        :param int expiry: URL validity time
        :param callable callback: Called function once done
        """
        session = botocore.session.get_session()
        client  = session.create_client('s3', region_name=self._region)

        url = client.generate_presigned_url(
            ClientMethod='get_object',
            Params={
                'Bucket': self._bucket,
                'Key':    path,
            },
            ExpiresIn=expiry,
            HttpMethod=method,
        )

        callback(url)

    @return_future
    def put(self, path, data, metadata={}, reduced_redundancy=False, encrypt_key=False, callback=None):
        """
        Stores data at given path
        :param string path: Path or 'key' for created/updated object
        :param bytes data: Data to write
        :param dict metadata: Metadata to store with this data
        :param bool reduced_redundancy: Whether to reduce storage redundancy or not?
        :param bool encrypt_key: Encrypt data?
        :param callable callback: Called function once done
        """
        storage_class = 'REDUCED_REDUNDANCY' if reduced_redundancy else 'STANDARD'

        args = dict(
            callback=callback,
            Bucket=self._bucket,
            Key=path,
            Body=data,
            Metadata=metadata,
            StorageClass=storage_class,
        )

        if encrypt_key:
            args['ServerSideEncryption'] = 'AES256'

        session = Botocore(service='s3', region_name=self._region, operation='PutObject')
        session.call(**args)

    @return_future
    def delete(self, path, callback=None):
        """
        Deletes key at given path
        :param string path: Path or 'key' to delete
        :param callable callback: Called function once done
        """
        session = Botocore(service='s3', region_name=self._region, operation='DeleteObject')
        session.call(
            callback=callback,
            Bucket=self._bucket,
            Key=path,
        )
