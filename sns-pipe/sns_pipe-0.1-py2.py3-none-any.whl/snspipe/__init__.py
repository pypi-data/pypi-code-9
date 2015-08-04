#!/usr/bin/env python

import boto3
import collections
import json
import sys


EXIT_STATUS_SUCCESS = 0
EXIT_STATUS_INCORRECT_USAGE = 3
EXIT_STATUS_INVALID_ARGUMENT = 4
EXIT_STATUS_BAD_RESPONSE = 5
EXIT_STATUS_TESTS_FAILED = 6


ARN = collections.namedtuple(
    typename='ARN',
    field_names='arn partition service region account resource',
)


def parse_arn(arn):
    fields = arn.split(':')
    try:
        return ARN(*fields)
    except Exception:
        raise ValueError(
            'ARNs must be in the format ' + ':'.join(ARN._fields)
        )


def publish(topic_arn, subject, body):

    region_name = parse_arn(topic_arn).region

    sns = boto3.resource('sns', region_name=region_name)
    topic = sns.Topic(topic_arn)

    response = topic.publish(
        Subject=subject,
        Message=body,
    )

    http_status_code = response.get('ResponseMetadata', {}).get('HTTPStatusCode')
    message_id = response.get('MessageId')
    response_ok = bool(http_status_code == 200 and message_id)

    try:
        response_str = json.dumps(response, indent=2)
    except Exception:
        response_ok = False
        response_str = repr(response)

    if response_ok:
        sys.stdout.write(response_str)
        sys.stdout.write('\n')
    else:
        sys.stderr.write(response_str)
        sys.stderr.write('\n')
        sys.exit(EXIT_STATUS_BAD_RESPONSE)


def read_stdin():
    stdin = sys.stdin.readlines()
    lines = [line.strip() for line in stdin]
    lines = [line for line in lines if line]
    if lines:
        subject = lines[0]
    else:
        subject = ''
    if len(subject) > 60:
        subject = truncate(subject, 50)
        body = '\n'.join(lines)
    else:
        body = '\n'.join(lines[1:])
    if not body:
        body = subject
    return (subject, body)


def test():
    import doctest

    failure_count, test_count = doctest.testmod()

    if failure_count:
        return False

    sys.stdout.write('{} passed and 0 failed.\n'.format(test_count))

    if test_count:
        sys.stdout.write('Test passed.\n')
        return True
    else:
        sys.stdout.write('***Test Failed*** no tests found.\n')
        return False


def truncate(text, length, etc='...'):
    """
    Truncates a line of text to the specified length.

    Truncate where text is already short enough:
    >>> truncate('abc', 10)
    'abc'

    Basic truncate:
    >>> truncate('abcdefgh', 8)
    'abcde...'

    Truncate chooses a space which is more than half way through the text:
    >>> truncate('abcdefg hijkl', 10)
    'abcdefg...'
    >>> truncate('abcdefg hijkl', 11)
    'abcdefg...'
    >>> truncate('abcdefg hijkl', 12)
    'abcdefg...'
    >>> truncate('abcdefg hijkl', 13)
    'abcdefg...'

    Truncate ignores a space because it is in the first half of the text:
    >>> truncate('abc defghijkl', 10)
    'abc def...'

    Truncate with a different suffix:
    >>> truncate('abcdefghijkl', 5, etc='!')
    'abcd!'

    """

    if length > len(text):
        return text

    length -= len(etc)

    text = text[:length]

    if text[-1] == ' ':
        return text.strip() + etc

    try:
        last_space = text.rindex(' ')
    except ValueError:
        last_space = 0

    if last_space > length // 2:
        text = text[:last_space]

    return text + etc
