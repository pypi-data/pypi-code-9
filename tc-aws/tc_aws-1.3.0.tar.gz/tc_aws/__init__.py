# coding: utf-8

from thumbor.config import Config

Config.define('STORAGE_BUCKET',                         'thumbor-images',   'S3 bucket for Storage', 'S3')
Config.define('RESULT_STORAGE_BUCKET',                  'thumbor-result',   'S3 bucket for result Storage', 'S3')
Config.define('S3_LOADER_BUCKET',                       None,               'S3 bucket for loader', 'S3')

Config.define('S3_LOADER_ROOT_PATH',                    '',                 'S3 path prefix for Loader bucket', 'S3')
Config.define('STORAGE_AWS_STORAGE_ROOT_PATH',          '',                 'S3 path prefix for Storage bucket', 'S3')
Config.define('RESULT_STORAGE_AWS_STORAGE_ROOT_PATH',   '',                 'S3 path prefix for Result storage bucket', 'S3')

Config.define('STORAGE_EXPIRATION_SECONDS',             3600,               'S3 expiration', 'S3')

Config.define('S3_STORAGE_SSE',                         False,              'S3 encriptipon key', 'S3')
Config.define('S3_STORAGE_RRS',                         False,              'S3 redundency', 'S3')
Config.define('S3_ALLOWED_BUCKETS',                     False,              'List of allowed bucket to be requeted', 'S3')
Config.define('RESULT_STORAGE_S3_STORE_METADATA',       False,              'S3 store result with metadata', 'S3')

Config.define('AWS_ACCESS_KEY',                         None,               'AWS Access key, if None use environment AWS_ACCESS_KEY_ID', 'AWS')
Config.define('AWS_SECRET_KEY',                         None,               'AWS Secret key, if None use environment AWS_SECRET_ACCESS_KEY', 'AWS')
Config.define('AWS_ROLE_BASED_CONNECTION',              False,              'EC2 instance can use role that does not require AWS_ACCESS_KEY see http://docs.aws.amazon.com/IAM/latest/UserGuide/roles-usingrole-ec2instance.html', 'AWS')

Config.define('BOTO_CONFIG',                            None,               'Additional Boto options for configuring S3 access (see http://boto.readthedocs.org/en/latest/ref/s3.html?highlight=boto.s3.connection.s3connection#boto.s3.connection.S3Connection)')
