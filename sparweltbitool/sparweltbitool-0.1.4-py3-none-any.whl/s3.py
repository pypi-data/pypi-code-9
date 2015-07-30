from boto.s3.connection import S3Connection
import boto
from sparweltbitool.config import config
from sparweltbitool.logger import Logger

class S3Client():
    """
    Operations with s3 bucket.
    Check documentation: http://boto.readthedocs.org/en/latest/ref/s3.html
    """

    def __init__(self):
        self.conn = S3Connection(config.get('aws', 'access_key_id'), config.get('aws', 'secret_access_key'))
        self.logger = Logger()

    def send_file_local(self, key, file_path_local):
        """ Fetch all  files for current user."""
        conn = self.conn

        message = "Sending local file: '{}' under a key: '{}' on s3 bucket: '{}' set on region: '{}'".format(
            file_path_local,
            key,
            config.get('aws', 'bucket'),
            config.get('aws', 'region'))

        Logger().debug(message)

        bucket = conn.get_bucket(config.get('aws', 'bucket'))
        if not bucket.get_location():
            conn = boto.s3.connect_to_region(config.get('aws', 'region'))
            bucket = conn.get_bucket(config.get('aws', 'bucket'))

        return bucket.new_key(key).set_contents_from_filename(file_path_local)

    def rename_files(self, prefix_old, prefix_new):
        """ Copy all keys from prefix_old to exact keys with prefix_new. Then delete original keys."""
        conn = self.conn

        bucket = conn.get_bucket(config.get('aws', 'bucket'))
        bucket_entries = bucket.list(prefix=prefix_old)

        count = 0

        for entry in bucket_entries:
            new_key_name = entry.name.replace(prefix_old, prefix_new)
            entry.copy(config.get('aws', 'bucket'), new_key_name)
            entry.delete()
            count += 1

        if count > 0:
            message = "{} files renamed from prefix: '{}' to new prefix: '{}' on s3 bucket: '{}' set on region: '{}'".format(
                count,
                prefix_old,
                prefix_new,
                config.get('aws', 'bucket'),
                config.get('aws', 'region'))
        else:
            message = "Tried to rename files from prefix: '{}' to new prefix: '{}' on s3 bucket: '{}' set on region: '{}' but none found.".format(
                prefix_old,
                prefix_new,
                config.get('aws', 'bucket'),
                config.get('aws', 'region'))

        Logger().debug(message)
