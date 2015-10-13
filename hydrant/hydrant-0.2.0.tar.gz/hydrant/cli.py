import botocore.session
import click


DEFAULT_AWS_REGION = 'us-east-1'


@click.command(epilog='Source: https://github.com/bwbaugh/hydrant')
@click.argument('delivery_stream')
@click.option(
    '--region',
    default=DEFAULT_AWS_REGION,
    help='The region to use. The delivery stream must be in this region.',
    show_default=True,
    metavar='AWS_REGION',
)
@click.version_option()
def main(delivery_stream, region):
    """Redirects stdin to Amazon Kinesis Firehose.

    Records will be written to DELIVERY_STREAM. Data should be
    separated by a newline character. Each line will be sent as a
    separate record, so keep in mind that Kinesis Firehose will round
    up each record to the next 5 KB in size.
    """
    client = _get_firehose_client(region_name=region)
    for line in click.get_binary_stream('stdin'):
        client.put_record(
            DeliveryStreamName=delivery_stream,
            Record={'Data': line},
        )


def _get_firehose_client(region_name):
    session = botocore.session.get_session()
    client = session.create_client(
        service_name='firehose',
        region_name=region_name,
    )
    return client
