#se!/usr/bin/python
# -*- coding: utf-8 -*-
from mock import Mock

from pyvows import Vows, expect
from mock import patch

from thumbor.context import Context
from derpconf.config import Config

import boto
from boto.s3.key import Key

from moto import mock_s3

from fixtures.storage_fixture import IMAGE_PATH, IMAGE_BYTES

from tc_aws.loaders import s3_loader

s3_bucket = 'thumbor-images-test'


@Vows.batch
class S3LoaderVows(Vows.Context):

    class CanLoadImage(Vows.Context):
        @mock_s3
        def topic(self):
            conn = boto.connect_s3()
            bucket = conn.create_bucket(s3_bucket)

            k = Key(bucket)
            k.key = IMAGE_PATH
            k.set_contents_from_string(IMAGE_BYTES)

            conf = Config()
            conf.define('S3_LOADER_BUCKET', s3_bucket, '')
            conf.define('S3_LOADER_ROOT_PATH', 'root_path', '')

            return Context(config=conf)

    def should_load_from_s3(self, topic):
        image = yield s3_loader.load(topic, '/'.join(['root_path', IMAGE_PATH]))
        expect(image).to_equal(IMAGE_BYTES)

    class ValidatesBuckets(Vows.Context):
        def topic(self):
            conf = Config()
            conf.define('S3_ALLOWED_BUCKETS', [], '')

            return Context(config=conf)

        def should_load_from_s3(self, topic):
            image = yield s3_loader.load(topic, '/'.join([s3_bucket, IMAGE_PATH]))
            expect(image).to_equal(None)

    class HandlesHttpLoader(Vows.Context):
        def topic(self):
            conf = Config()
            conf.define('AWS_ENABLE_HTTP_LOADER', True, '')

            return Context(config=conf)

        def should_redirect_to_http(self, topic):
            with patch('thumbor.loaders.http_loader.load_sync') as mock_load_sync:
                yield s3_loader.load(topic, 'http://foo.bar')
                expect(mock_load_sync.called).to_be_true()

    class CanDetectBucket(Vows.Context):
        def topic(self):
            return s3_loader._get_bucket('/'.join([s3_bucket, IMAGE_PATH]))

        def should_detect_bucket(self, topic):
            expect(topic[0]).to_equal(s3_bucket)
            expect(topic[1]).to_equal(IMAGE_PATH)

    class CanNormalize(Vows.Context):
        def topic(self):
            return s3_loader._normalize_url('/'.join([s3_bucket, IMAGE_PATH]))

        def should_detect_bucket(self, topic):
            expect(topic).to_equal('/'.join([s3_bucket, IMAGE_PATH]))
