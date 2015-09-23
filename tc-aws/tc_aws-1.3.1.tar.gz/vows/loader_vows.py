# se!/usr/bin/python
# -*- coding: utf-8 -*-
from mock import Mock

from pyvows import Vows, expect

from thumbor.context import Context
from derpconf.config import Config

import boto
from boto.s3.key import Key

from moto import mock_s3

from fixtures.storage_fixture import IMAGE_PATH, IMAGE_BYTES

from tc_aws.loaders import *

s3_bucket = 'thumbor-images-test'


@Vows.batch
class S3LoaderVows(Vows.Context):

    class CanGetBucketAndKey(Vows.Context):

        def topic(self):
            conf = Config()
            conf.S3_LOADER_BUCKET = None
            conf.S3_LOADER_ROOT_PATH = ''
            return Context(config=conf)

        def should_detect_bucket_and_key(self, topic):
            path = 'some-bucket/some/image/path.jpg'
            bucket, key = _get_bucket_and_key(topic, path)
            expect(bucket).to_equal('some-bucket')
            expect(key).to_equal('/some/image/path.jpg')

    class CanDetectBucket(Vows.Context):

        def topic(self):
            return _get_bucket('/'.join([s3_bucket, IMAGE_PATH]))

        def should_detect_bucket(self, topic):
            expect(topic[0]).to_equal(s3_bucket)
            expect(topic[1]).to_equal(IMAGE_PATH)

    class CanNormalize(Vows.Context):

        def topic(self):
            return _normalize_url('/'.join([s3_bucket, IMAGE_PATH]))

        def should_detect_bucket(self, topic):
            expect(topic).to_equal('/'.join([s3_bucket, IMAGE_PATH]))
