#se!/usr/bin/python
# -*- coding: utf-8 -*-

from pyvows import Vows, expect

from thumbor.context import Context
from thumbor.config import Config
from fixtures.storage_fixture import IMAGE_URL, IMAGE_BYTES, get_server
import time

from boto.s3.connection import S3Connection
from boto.s3.key import Key
from moto import mock_s3

from tc_aws.storages.s3_storage import Storage

s3_bucket = 'thumbor-images-test'


@Vows.batch
class S3StorageVows(Vows.Context):

    class CanStoreImage(Vows.Context):
        @mock_s3
        def topic(self):
            self.conn = S3Connection()
            bucket = self.conn.create_bucket(s3_bucket)

            thumborId = IMAGE_URL % '1'
            config = Config(STORAGE_BUCKET=s3_bucket)
            storage = Storage(Context(config=config, server=get_server('ACME-SEC')))
            store = storage.put(thumborId, IMAGE_BYTES)
            k = Key(bucket)
            k.key = thumborId
            result = k.get_contents_as_string()
            return (store, result)

        def should_be_in_catalog(self, topic):
            expect(topic[0]).to_equal(IMAGE_URL % '1')
            expect(topic[1]).not_to_be_null()
            expect(topic[1]).not_to_be_an_error()
            expect(topic[1]).to_equal(IMAGE_BYTES)

    class CanGetImage(Vows.Context):
        @mock_s3
        def topic(self):
            self.conn = S3Connection()
            self.conn.create_bucket(s3_bucket)

            config = Config(STORAGE_BUCKET=s3_bucket)
            storage = Storage(Context(config=config, server=get_server('ACME-SEC')))
            storage.put(IMAGE_URL % '2', IMAGE_BYTES)
            return storage.get(IMAGE_URL % '2')

        def should_not_be_null(self, topic):
            expect(topic).not_to_be_null()
            expect(topic).not_to_be_an_error()

        def should_have_proper_bytes(self, topic):
            expect(topic).to_equal(IMAGE_BYTES)

    class CanGetImageExistance(Vows.Context):
        @mock_s3
        def topic(self):
            self.conn = S3Connection()
            self.conn.create_bucket(s3_bucket)

            config = Config(STORAGE_BUCKET=s3_bucket)
            storage = Storage(Context(config=config, server=get_server('ACME-SEC')))
            storage.put(IMAGE_URL % '3', IMAGE_BYTES)
            return storage.exists(IMAGE_URL % '3')

        def should_exists(self, topic):
            expect(topic).to_equal(True)

    class CanGetImageInexistance(Vows.Context):
        @mock_s3
        def topic(self):
            self.conn = S3Connection()
            self.conn.create_bucket(s3_bucket)

            config = Config(STORAGE_BUCKET=s3_bucket)
            storage = Storage(Context(config=config, server=get_server('ACME-SEC')))
            return storage.exists(IMAGE_URL % '9999')

        def should_not_exists(self, topic):
            expect(topic).to_equal(False)

    class CanRemoveImage(Vows.Context):
        @mock_s3
        def topic(self):
            self.conn = S3Connection()
            self.conn.create_bucket(s3_bucket)

            config = Config(STORAGE_BUCKET=s3_bucket)
            storage = Storage(Context(config=config, server=get_server('ACME-SEC')))
            storage.put(IMAGE_URL % '4', IMAGE_BYTES)
            created = storage.exists(IMAGE_URL % '4')
            time.sleep(1)
            storage.remove(IMAGE_URL % '4')
            time.sleep(1)
            return storage.exists(IMAGE_URL % '4') != created

        def should_be_put_and_removed(self, topic):
            expect(topic).to_equal(True)

    class CanRemovethenPutImage(Vows.Context):
        @mock_s3
        def topic(self):
            self.conn = S3Connection()
            self.conn.create_bucket(s3_bucket)

            config = Config(STORAGE_BUCKET=s3_bucket)
            storage = Storage(Context(config=config, server=get_server('ACME-SEC')))
            storage.put(IMAGE_URL % '5', IMAGE_BYTES)
            storage.remove(IMAGE_URL % '5')
            time.sleep(1)
            created = storage.exists(IMAGE_URL % '5')
            time.sleep(1)
            storage.put(IMAGE_URL % '5', IMAGE_BYTES)
            return storage.exists(IMAGE_URL % '5') != created

        def should_be_put_and_removed(self, topic):
            expect(topic).to_equal(True)

    class CanReturnPath(Vows.Context):
        @mock_s3
        def topic(self):
            self.conn = S3Connection()
            self.conn.create_bucket(s3_bucket)

            config = Config(STORAGE_BUCKET=s3_bucket)
            storage = Storage(Context(config=config, server=get_server('ACME-SEC')))
            return storage.resolve_original_photo_path("toto")

        def should_return_the_same(self, topic):
            expect(topic).to_equal("toto")

    class HandlesStoragePrefix(Vows.Context):
        @mock_s3
        def topic(self):
            self.conn = S3Connection()
            self.conn.create_bucket(s3_bucket)

            config = Config(STORAGE_BUCKET=s3_bucket, STORAGE_AWS_STORAGE_ROOT_PATH='tata')
            storage = Storage(Context(config=config, server=get_server('ACME-SEC')))

            return storage.normalize_path('toto')

        def should_return_the_same(self, topic):
            expect(topic).to_equal("tata/toto")

    class CryptoVows(Vows.Context):
        class RaisesIfInvalidConfig(Vows.Context):
            @Vows.capture_error
            @mock_s3
            def topic(self):
                self.conn = S3Connection()
                self.conn.create_bucket(s3_bucket)

                config = Config(STORAGE_BUCKET=s3_bucket, STORES_CRYPTO_KEY_FOR_EACH_IMAGE=True)
                storage = Storage(Context(config=config, server=get_server('')))
                storage.put(IMAGE_URL % '9999', IMAGE_BYTES)
                storage.put_crypto(IMAGE_URL % '9999')

            def should_be_an_error(self, topic):
                expect(topic).to_be_an_error_like(RuntimeError)
                expect(topic).to_have_an_error_message_of("STORES_CRYPTO_KEY_FOR_EACH_IMAGE can't be True if no SECURITY_KEY specified")

        class GettingCryptoForANewImageReturnsNone(Vows.Context):
            @mock_s3
            def topic(self):
                self.conn = S3Connection()
                self.conn.create_bucket(s3_bucket)

                config = Config(STORAGE_BUCKET=s3_bucket, STORES_CRYPTO_KEY_FOR_EACH_IMAGE=True)
                storage = Storage(Context(config=config, server=get_server('ACME-SEC')))
                return storage.get_crypto(IMAGE_URL % '9999')

            def should_be_null(self, topic):
                expect(topic).to_be_null()

        class DoesNotStoreIfConfigSaysNotTo(Vows.Context):
            @mock_s3
            def topic(self):
                self.conn = S3Connection()
                self.conn.create_bucket(s3_bucket)

                config = Config(STORAGE_BUCKET=s3_bucket)
                storage = Storage(Context(config=config, server=get_server('ACME-SEC')))
                storage.put(IMAGE_URL % '9998', IMAGE_BYTES)
                storage.put_crypto(IMAGE_URL % '9998')
                return storage.get_crypto(IMAGE_URL % '9998')

            def should_be_null(self, topic):
                expect(topic).to_be_null()

        class CanStoreCrypto(Vows.Context):
            @mock_s3
            def topic(self):
                self.conn = S3Connection()
                self.conn.create_bucket(s3_bucket)

                config = Config(STORAGE_BUCKET=s3_bucket, STORES_CRYPTO_KEY_FOR_EACH_IMAGE=True)
                storage = Storage(Context(config=config, server=get_server('ACME-SEC')))
                storage.put(IMAGE_URL % '6', IMAGE_BYTES)
                storage.put_crypto(IMAGE_URL % '6')
                return storage.get_crypto(IMAGE_URL % '6')

            def should_not_be_null(self, topic):
                expect(topic).not_to_be_null()
                expect(topic).not_to_be_an_error()

            def should_have_proper_key(self, topic):
                expect(topic).to_equal('ACME-SEC')

    class DetectorVows(Vows.Context):
        class CanStoreDetectorData(Vows.Context):
            @mock_s3
            def topic(self):
                self.conn = S3Connection()
                self.conn.create_bucket(s3_bucket)

                config = Config(STORAGE_BUCKET=s3_bucket)
                storage = Storage(Context(config=config, server=get_server('ACME-SEC')))
                storage.put(IMAGE_URL % '7', IMAGE_BYTES)
                storage.put_detector_data(IMAGE_URL % '7', 'some-data')
                return storage.get_detector_data(IMAGE_URL % '7')

            def should_not_be_null(self, topic):
                expect(topic).not_to_be_null()
                expect(topic).not_to_be_an_error()

            def should_equal_some_data(self, topic):
                expect(topic).to_equal('some-data')

        class ReturnsNoneIfNoDetectorData(Vows.Context):
            @mock_s3
            def topic(self):
                self.conn = S3Connection()
                self.conn.create_bucket(s3_bucket)

                config = Config(STORAGE_BUCKET=s3_bucket)
                storage = Storage(Context(config=config, server=get_server('ACME-SEC')))
                return storage.get_detector_data(IMAGE_URL % '9999')

            def should_not_be_null(self, topic):
                expect(topic).to_be_null()
