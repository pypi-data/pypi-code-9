
import boto
from moto import mock_s3, mock_emr
from datacanvas.clusters import EmrCluster


def test_hello_world():
    pass

@mock_s3
@mock_emr
def test_emr_cluster():
    s3_conn = boto.connect_s3()
    # We need to create the bucket since this is all in Moto's 'virtual' AWS account
    s3_conn.create_bucket('mybucket')

    # EMR
    emr_conn = boto.connect_emr()
    cluster_id = emr_conn.run_jobflow(name="")
    print cluster_id

    # emr_cluster = EmrCluster(aws_region = "ap-southeast-1",
    #                          aws_key = "aws_key",
    #                          aws_secret = "aws_sec",
    #                          jobflow_id = cluster_id)

    emr_cluster = EmrCluster(aws_region = "ap-southeast-1",
                             aws_key = "aws_key",
                             aws_secret = "aws_sec",
                             jobflow_id = cluster_id)

    print "emr_conn...."
    print emr_cluster.emr_conn
    # print emr_cluster.s3_list_files("s3://mybucket/")
    # emr_cluster.execute_jar("job_name", "s3://mybucket/kaka.jar")

