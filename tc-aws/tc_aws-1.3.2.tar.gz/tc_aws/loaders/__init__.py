# coding: utf-8
__all__ = ['_get_bucket_and_key', '_get_bucket', '_get_key', '_normalize_url', '_validate_bucket', '_use_http_loader']

import urllib2


def _get_bucket_and_key(context, url):
    url = urllib2.unquote(url)

    bucket = context.config.get('S3_LOADER_BUCKET')
    if bucket is None:
        bucket = _get_bucket(url)
        url = '/'.join(url.lstrip('/').split('/')[1:])

    key = _get_key(url, context)

    return bucket, key


def _get_bucket(url):
    url_by_piece = url.lstrip("/").split("/")

    return url_by_piece[0]


def _get_key(path, context):
    root_path = context.config.get('S3_LOADER_ROOT_PATH')
    return '/'.join([root_path, path]) if root_path is not '' else path


def _normalize_url(url):
    """
    :param url:
    :return: exactly the same url since we only use http loader if url stars with http prefix.
    """
    return url


def _validate_bucket(context, bucket):
    allowed_buckets = context.config.get('S3_ALLOWED_BUCKETS', default=None)
    return not allowed_buckets or bucket in allowed_buckets


def _use_http_loader(context, url):
    enable_http_loader = context.config.get('AWS_ENABLE_HTTP_LOADER', default=False)
    return enable_http_loader and url.startswith('http')
