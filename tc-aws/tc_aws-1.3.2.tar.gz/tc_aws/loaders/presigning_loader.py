# coding: utf-8

from boto.s3.bucket import Bucket
from thumbor.utils import logger
from tornado.concurrent import return_future

import thumbor.loaders.http_loader as http_loader

from tc_aws.loaders import *
from tc_aws.aws.connection import get_connection


def _generate_presigned_url(context, bucket, key):
    connection = get_connection(context)
    expiry = 60 * 60
    presigned_url = connection.generate_url(
        expiry,
        'GET',
        bucket,
        key,
    )
    return presigned_url


@return_future
def load(context, url, callback):
    load_sync(context, url, callback)


def load_sync(context, url, callback):
    if _use_http_loader(context, url):
        http_loader.load_sync(
            context, url, callback, normalize_url_func=_normalize_url)
    else:
        bucket, key = _get_bucket_and_key(context, url)

        if _validate_bucket(context, bucket):
            presigned_url = _generate_presigned_url(context, bucket, key)
            http_loader.load_sync(
                context, presigned_url, callback, normalize_url_func=_normalize_url)
        else:
            callback(None)
