# -*- coding: utf-8 -*-
'''
AWS metadata backend.

Arguments: None

Defines the following values on AWS EC2 instances:

 *  aws_instance_id
 *  aws_availability_zone
 *  aws_instance_type
 *  aws_local_ipv4
 *  aws_public_ipv4
'''

import logging
import requests

METADATA_SERVICE_URL = 'http://169.254.169.254/latest/meta-data'
DEFAULT_METADATA_SERVICE_TIMEOUT = 1

log = logging.getLogger(__name__)
description = 'Defines variables from AWS metadata'


class RetriesExceededError(Exception):
    '''Internal exception used when the number of retries are exceeded.'''
    pass


def metadata(path, timeout=None, num_attempts=None):
    if not timeout:
        timeout = DEFAULT_METADATA_SERVICE_TIMEOUT
    if not num_attempts:
        num_attempts = 1

    url = "/".join((METADATA_SERVICE_URL, path))
    for i in range(num_attempts):
        try:
            log.debug('Requesting metadata at {}'.format(url))
            response = requests.get(url, timeout=timeout)
        except (requests.Timeout, requests.ConnectionError) as e:
            log.debug('Caught exception while trying to retrieve metadata: '
                      '%s', e, exc_info=True)
        else:
            if response.status_code == 200:
                return response.content.decode('utf-8')
        raise RetriesExceededError()


def context():
    '''Gather AWS metadata about the current instance'''
    log.info('Gathering AWS metadata')
    try:
        return {
            'aws_instance_id': metadata('instance-id'),
            'aws_availability_zone': metadata('placement/availability-zone'),
            'aws_instance_type': metadata('instance-type'),
            'aws_local_ipv4': metadata('local-ipv4'),
            'aws_public_ipv4': metadata('public-ipv4'),
        }
    except RetriesExceededError:
        return {}
