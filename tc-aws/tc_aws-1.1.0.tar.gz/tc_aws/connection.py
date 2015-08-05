# coding: utf-8

from boto.s3.connection import S3Connection

connection = None

def get_connection(context):
    conn = connection
    if conn is None:
        boto_opts = {}

        if context.config.AWS_ROLE_BASED_CONNECTION==False:
            boto_opts.update({
                'aws_access_key_id'    : context.config.AWS_ACCESS_KEY,
                'aws_secret_access_key': context.config.AWS_SECRET_KEY,
                })

        if context.config.BOTO_CONFIG:
            boto_opts.update(context.config.BOTO_CONFIG)

        conn = S3Connection(**boto_opts)

    return conn
