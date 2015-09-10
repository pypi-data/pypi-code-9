'''
Created on Sep 4, 2015

@author: andrei
'''

import os, sys
import tools.auxiliary as auxiliary
from boto.s3.connection import S3Connection, OrdinaryCallingFormat

try:
    CLAUDE_ROOT = os.environ['CLAUDE_ROOT']
    sys.path.append(os.path.join(CLAUDE_ROOT, 'claude_core'))
except KeyError:
    print 'No CLAUDE_ROOT environmental variable is specified'
except:
    raise

def s3cmdGET(s3cfg_path, s3_path, local_path, shellOutput=True):
    cmd = "s3cmd -c %s get %s %s" %(s3cfg_path, s3_path, local_path)
    auxiliary.execute(cmd, shellOutput=shellOutput)
    
def s3cmdPUT(s3cfg_path, local_path, s3_path, shellOutput=True):
    cmd = "s3cmd -c %s put %s %s" %(s3cfg_path, local_path, s3_path)
    auxiliary.execute(cmd, shellOutput=shellOutput)
    
def botoGetURL(filepath):
    config = auxiliary.readConfig(os.path.join(CLAUDE_ROOT, 'claude_config/claude.cfg'))
    
    AWS_ACCESS_KEY_ID = auxiliary.read_option(config, 'aws', 'aws_access_key')
    AWS_SECRET_ACCESS_KEY = auxiliary.read_option(config, 'aws', 'aws_secret_key')
    AWS_S3_HOST = auxiliary.read_option(config, 'aws', 'aws_s3_host')
    AWS_S3_PORT = int(auxiliary.read_option(config, 'aws', 'aws_s3_port'))
    AWS_S3_USE_SSL = auxiliary.str2bool(auxiliary.read_option(config, 'aws', 'aws_s3_use_ssl'))
    AWS_STORAGE_BUCKET_NAME = auxiliary.read_option(config, 'aws', 'aws_storage_bucket_name')
    
    conn = S3Connection(
                    aws_access_key_id=AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                    host=AWS_S3_HOST,
                    port=AWS_S3_PORT,
                    is_secure=AWS_S3_USE_SSL,
                    calling_format=OrdinaryCallingFormat()
                    )
    
    url = conn.generate_url(60, 'GET',
                            bucket=AWS_STORAGE_BUCKET_NAME,
                            key=filepath,
                            force_http=False)
    
    return url   