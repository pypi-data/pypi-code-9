# coding: utf-8
from __future__ import with_statement
from functools import wraps
import codecs
import json
import os
import platform
import re
import subprocess
import sys
import time

from fabric.api import *
from fabric.colors import *
from fabric.utils import abort
from fabric.contrib.console import confirm

from .fab_utils import *


def get_bucket_policy(bucket, host):
    policy = """
    {
      "Version":"2012-10-17",
      "Id":"http referer policy example",
      "Statement":[
        {
          "Sid":"Allow get requests originated from www.example.com and example.com",
          "Effect":"Allow",
          "Principal":"*",
          "Action":"s3:GetObject",
          "Resource":"arn:aws:s3:::%s/*",
          "Condition":{
            "StringLike":{"aws:Referer":["http://www.%s/*","http://%s/*","https://www.%s/*","https://%s/*"]}
          }
        }
      ]
    }""" % (bucket, host, host, host, host)
    return policy.strip()

def get_or_create_bucket(name, public=True, cors=None):
    import boto
    from boto.s3.cors import CORSConfiguration
    conn = boto.connect_s3() # read AWS env vars
    bucket = conn.lookup(name)
    if bucket is None:
        print('Creating bucket %s' % name)
        bucket = conn.create_bucket(name)
        if public:
            bucket.set_acl('public-read')
        if cors:
            cors_cfg = CORSConfiguration()
            cors_cfg.add_rule(['GET', 'POST'], 'http://*', allowed_header='*', max_age_seconds=604800)
            cors_cfg.add_rule(['GET', 'POST'], 'https://*', allowed_header='*', max_age_seconds=604800)
            cors_cfg.add_rule('GET', '*', allowed_header='*', max_age_seconds=604800)
            bucket.set_cors(cors_cfg)
            bucket.set_policy(get_bucket_policy(name, cors), headers=None)
    return bucket

def upload_file_to_s3(bucket_name, filename, public=True, static_headers=False, gzip=False):
    bucket = get_or_create_bucket(bucket_name, cors=True)
    print('Uploading %s to Amazon S3 bucket %s' % (filename, bucket_name))
    k = bucket.new_key(filename)
    if static_headers:
        content_types = {
            '.gz': 'application/x-gzip',
            '.js': 'application/x-javascript',
            '.map': 'application/json',
            '.json': 'application/json',
            '.css': 'text/css',
            '.html': 'text/html',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.gif': 'image/gif',
            '.png': 'image/png',
            '.pdf': 'application/pdf',
        }
        dir_filename, extension = os.path.splitext(filename)
        k.set_metadata('Content-Type', content_types.get(extension, 'text/plain'))
        k.set_metadata('Cache-Control', 'max-age=31536000')
        k.set_metadata('Expires', 'Thu, 31 Dec 2015 23:59:59 GM') # FIXME parameter timedelta 1year
        if gzip:
            k.set_metadata('Content-Encoding', 'gzip')
    def percent_cb(complete, total):
        sys.stdout.write('.')
        sys.stdout.flush()
    k.set_contents_from_filename(filename, cb=percent_cb, num_cb=10)
    if public:
        k.set_acl('public-read')

def upload_js(bucket_name, filename, minify=True, gzip=True):
    if minify:
        fmin, fmap = minify_js(filename)
        upload_file_to_s3(bucket_name, fmin, public=True, static_headers=True, gzip=False)
        upload_file_to_s3(bucket_name, fmap, public=True, static_headers=True, gzip=False)
        if gzip:
            upload_file_to_s3(bucket_name, compress(fmin), public=True, static_headers=True, gzip=True)
            upload_file_to_s3(bucket_name, compress(fmap), public=True, static_headers=True, gzip=True)
    if gzip:
        upload_file_to_s3(bucket_name, compress(filename), public=True, static_headers=True, gzip=True)
    upload_file_to_s3(bucket_name, filename, public=True, static_headers=True, gzip=False)

def upload_css(bucket_name, filename, gzip=True):
    if gzip:
        filename_gz = compress(filename)
        upload_file_to_s3(bucket_name, filename_gz, public=True, static_headers=True, gzip=True)
    upload_file_to_s3(bucket_name, filename, public=True, static_headers=True, gzip=False)

def upload_file(bucket_name, filename):
    if filename.endswith('.js'):
        upload_js(bucket_name, filename)
    elif filename.endswith('.css'):
        upload_css(bucket_name, filename)
    elif filename.endswith('.jpg') or filename.endswith('.jpeg') or filename.endswith('.gif') or filename.endswith('.png'):
        upload_file_to_s3(bucket_name, filename, public=True, static_headers=True, gzip=False)
    else:
        upload_file_to_s3(bucket_name, filename, public=True, static_headers=False, gzip=False)

@task
def upload_static_files(folder='static'):
    print(red("Uploading static files to S3"))
    for (current_dir, dirs, files) in os.walk(folder):
        for filename in files:
            block = ['.gz', '.min', '.map']
            skip = False
            for b in block:
                if b in filename:
                    skip = True
                    break
            if not skip:
                path = os.path.join(current_dir, filename)
                upload_file(env.aws_bucket, path)
    print(red("Uploaded succesful"))
