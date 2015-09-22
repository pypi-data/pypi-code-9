# coding: utf-8

import calendar

from os.path import join

from datetime import datetime, timedelta

from thumbor.utils import logger

from boto.s3.bucket import Bucket
from boto.s3.key import Key
from dateutil.parser import parse as parse_ts

from connection import get_connection


class AwsStorage():

    @property
    def is_auto_webp(self):
        return self.context.config.AUTO_WEBP and self.context.request.accepts_webp

    def __init__(self, context, config_prefix):
        self.config_prefix = config_prefix
        self.context = context
        self.storage = self.__get_s3_bucket()

    def _get_config(self, config_key, default=None):
        return getattr(self.context.config, '%s_%s' % (self.config_prefix, config_key))

    def __get_s3_bucket(self):
        return Bucket(
            connection=get_connection(self.context),
            name=self._get_config('BUCKET')
        )

    def set(self, bytes, abspath):
        file_key = Key(self.storage)
        file_key.key = abspath

        if self.config_prefix is 'RESULT_STORAGE' and self._get_config('S3_STORE_METADATA'):
            for k, v in self.context.headers.iteritems():
                file_key.set_metadata(k, v)

        file_key.set_contents_from_string(
            bytes,
            encrypt_key=self.context.config.get('S3_STORAGE_SSE', ''),         # TODO: fix config prefix
            reduced_redundancy=self.context.config.get('S3_STORAGE_RRS', '')   # TODO: fix config prefix
        )

    def get(self, path):
        file_abspath = self.normalize_path(path)

        file_key = self.storage.get_key(file_abspath)

        if not file_key or self.is_expired(file_key):
            logger.debug("[STORAGE] s3 key not found at %s" % file_abspath)
            return None
        return file_key.read()

    def normalize_path(self, path):
        path = path.lstrip('/')  # Remove leading '/'
        path_segments = [self._get_config('AWS_STORAGE_ROOT_PATH'), path]

        if self.is_auto_webp:
            path_segments.append("webp")

        return join(*path_segments)

    def is_expired(self, key):
        if key:
            expire_in_seconds = self._get_config('EXPIRATION_SECONDS')

            # Never expire
            if expire_in_seconds is None or expire_in_seconds == 0:
                return False

            timediff = datetime.now() - self.utc_to_local(parse_ts(key.last_modified))
            return timediff.seconds > self._get_config('EXPIRATION_SECONDS')
        else:
            #If our key is bad just say we're expired
            return True

    def last_updated(self):
        path = self.context.request.url
        file_abspath = self.normalize_path(path)
        file_key = self.storage.get_key(file_abspath)

        if not file_key or self.is_expired(file_key):
            logger.debug("[RESULT_STORAGE] s3 key not found at %s" % file_abspath)
            return None

        return self.utc_to_local(parse_ts(file_key.last_modified))

    def utc_to_local(self, utc_dt):
        # get integer timestamp to avoid precision lost
        timestamp = calendar.timegm(utc_dt.timetuple())
        local_dt = datetime.fromtimestamp(timestamp)
        assert utc_dt.resolution >= timedelta(microseconds=1)
        return local_dt.replace(microsecond=utc_dt.microsecond)
