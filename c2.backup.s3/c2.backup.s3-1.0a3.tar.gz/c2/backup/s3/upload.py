
import os
import math

import boto
from filechunkio import FileChunkIO


def upload_to_s3(aws_access_key, aws_secret_access_key, fileobj, bucket, path):
    """
    :param aws_access_key: str, AWS access key
    :param aws_secret_access_key: str, AWS secret
    :param fileobj: file object
    :param bucket: src, bukect name
    :param path: src, path of bucket
    :return: bool
    refer from "http://www.bogotobogo.com/DevOps/AWS/aws_S3_uploading_large_file.php"
    """
    source_path = fileobj.name
    try:
        source_size = os.fstat(fileobj.fileno()).st_size
    except:
        # Not all file objects implement fileno(),
        # so we fall back on this
        fileobj.seek(0, os.SEEK_END)
        source_size = fileobj.tell()

    # print 'source_size=%s MB' %(source_size/(1024*1024))

    conn = boto.connect_s3(aws_access_key, aws_secret_access_key)

    bucket = conn.get_bucket(bucket, validate=True)
    # print 'bucket=%s' %(bucket)

    # Create a multipart upload request
    backet_path = path
    mp = bucket.initiate_multipart_upload(backet_path)

    # Use a chunk size of 50 MiB (feel free to change this)
    chunk_size = 52428800
    chunk_count = int(math.ceil(source_size / chunk_size))
    # print 'chunk_count=%s' %(chunk_count)

    # Send the file parts, using FileChunkIO to create a file-like object
    # that points to a certain byte range within the original file. We
    # set bytes to never exceed the original file size.
    sent = 0
    for i in range(chunk_count + 1):
        offset = chunk_size * i
        bytes = min(chunk_size, source_size - offset)
        sent = sent +  bytes
        with FileChunkIO(source_path, 'r', offset=offset,
                         bytes=bytes) as fp:
            mp.upload_part_from_file(fp, part_num=i + 1)
        # print '%s: sent = %s MBytes ' %(i, sent/1024/1024)

    # Finish the upload
    mp.complete_upload()

    if sent == source_size:
        return True
    return False