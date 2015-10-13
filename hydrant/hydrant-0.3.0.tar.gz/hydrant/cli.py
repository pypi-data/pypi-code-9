import botocore.session
import click


DEFAULT_AWS_REGION = 'us-east-1'


@click.command(epilog='Source: https://github.com/bwbaugh/hydrant')
@click.version_option()
@click.argument('delivery_stream')
@click.option(
    '--region',
    default=DEFAULT_AWS_REGION,
    help='The region to use. The delivery stream must be in this region.',
    show_default=True,
    metavar='AWS_REGION',
)
@click.option(
    '--print-record-id/--no-print-record-id',
    default=False,
    help=(
        'Controls outputting the ID of each record, which is a unique '
        'string assigned to each record. Producer applications can '
        'use this ID for purposes such as auditability and '
        'investigation.'
    ),
)
def main(delivery_stream, region, print_record_id):
    """Redirects stdin to Amazon Kinesis Firehose.

    Records will be written to DELIVERY_STREAM. Data should be
    separated by a newline character. Each line will be sent as a
    separate record, so keep in mind that Kinesis Firehose will round
    up each record to the next 5 KB in size.

    The application submits each record one at a time, which limits the
    throughput to roughly ~15 records per second.

    The application submits each record one at a time, which limits the
    throughput. A future version might batch records together for
    performance, but until then beware of using high throughput streams
    (15 records per second or more). Running from within EC2 will allow
    higher throughput.
    """
    client = _get_firehose_client(region_name=region)
    for line in click.get_binary_stream('stdin'):
        response = client.put_record(
            DeliveryStreamName=delivery_stream,
            Record={'Data': line},
        )
        if print_record_id:
            click.echo(message=response['RecordId'])


def _get_firehose_client(region_name):
    session = botocore.session.get_session()
    client = session.create_client(
        service_name='firehose',
        region_name=region_name,
    )
    return client
