
import boto

def get_bucket_list(aws_access_key, aws_secret_access_key, bucket, prefix):
    """
    :param aws_access_key:
    :param aws_secret_access_key:
    :param bucket:
    :param prefix:
    :return: list of path
    """
    conn = boto.connect_s3(aws_access_key, aws_secret_access_key)
    bucket = conn.get_bucket(bucket, validate=True)
    result = bucket.list(prefix=prefix+"/")#, delimiter="/")
    return result
