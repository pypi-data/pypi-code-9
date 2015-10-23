import boto3

ec2 = boto3.resource('ec2')

print(ec2.create_tags.__doc__)

