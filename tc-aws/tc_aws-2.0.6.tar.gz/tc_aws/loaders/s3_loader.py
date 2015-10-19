# coding: utf-8

# Copyright (c) 2015, thumbor-community
# Use of this source code is governed by the MIT license that can be
# found in the LICENSE file.

from thumbor.utils import logger
from tornado.concurrent import return_future

import thumbor.loaders.http_loader as http_loader

from . import *
from ..aws.bucket import Bucket

@return_future
def load(context, url, callback):
    """
    Loads image
    :param Context context: Thumbor's context
    :param string url: Path to load
    :param callable callback: Callback method once done
    """
    if _use_http_loader(context, url):
        http_loader.load_sync(context, url, callback, normalize_url_func=_normalize_url)
        return

    bucket, key = _get_bucket_and_key(context, url)

    if _validate_bucket(context, bucket):
        bucket_loader = Bucket(bucket, context.config.get('TC_AWS_REGION'))

        def handle_data(file_key):
            if not file_key or 'Error' in file_key:
                logger.warn("ERROR retrieving image from S3 {0}: {1}".format(key, file_key['Error']['Message']))
            else:
                callback(file_key['Body'].read())

        bucket_loader.get(key, callback=handle_data)
    else:
        callback(None)
