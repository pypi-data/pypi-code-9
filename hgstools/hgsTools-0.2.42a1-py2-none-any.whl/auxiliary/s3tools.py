'''
Created on Jun 8, 2015

@author: andrei
'''

import os

from boto.s3.connection import S3Connection, OrdinaryCallingFormat
from boto.s3.key import Key

import hgsTools.auxiliary as auxiliary

def getConnection(config):
    AWS_ACCESS_KEY_ID = auxiliary.read_option(config, 'aws', 'aws_access_key')
    AWS_SECRET_ACCESS_KEY = auxiliary.read_option(config, 'aws', 'aws_secret_key')
    AWS_S3_HOST = auxiliary.read_option(config, 'aws', 'aws_s3_host')
    AWS_S3_PORT = int(auxiliary.read_option(config, 'aws', 'aws_s3_port'))
    AWS_S3_USE_SSL = auxiliary.str2bool(auxiliary.read_option(config, 'aws', 'aws_s3_use_ssl'))
    
    conn = S3Connection(
                    aws_access_key_id=AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                    host=AWS_S3_HOST,
                    port=AWS_S3_PORT,
                    is_secure=AWS_S3_USE_SSL,
                    calling_format=OrdinaryCallingFormat()
                    )
    return conn 

def uploadFile(config, local_file, remote_path):
    conn = getConnection(config)
    AWS_STORAGE_BUCKET_NAME = auxiliary.read_option(config, 'aws', 'aws_storage_bucket_name')
    bucket = conn.get_bucket(AWS_STORAGE_BUCKET_NAME)
    
    k = Key(bucket)
    k.key = os.path.join(remote_path, os.path.basename(local_file))

    k.set_contents_from_filename(local_file)
    
def downloadFile(config, remote_file, local_path):
    conn = getConnection(config)
    AWS_STORAGE_BUCKET_NAME = auxiliary.read_option(config, 'aws', 'aws_storage_bucket_name')
    bucket = conn.get_bucket(AWS_STORAGE_BUCKET_NAME)
    
    k = Key(bucket)
    k.key = remote_file
    
    k.get_contents_to_filename(os.path.join(local_path, os.path.basename(remote_file)))
    
def s3cmdGET(s3cfg_path, s3_path, local_path, shellOutput=True):
    cmd = "s3cmd -c %s get %s %s" %(s3cfg_path, s3_path, local_path)
    auxiliary.execute(cmd, shellOutput=shellOutput)
    
def s3cmdPUT(s3cfg_path, local_path, s3_path, shellOutput=True):
    cmd = "s3cmd -c %s put %s %s" %(s3cfg_path, local_path, s3_path)
    auxiliary.execute(cmd, shellOutput=shellOutput)