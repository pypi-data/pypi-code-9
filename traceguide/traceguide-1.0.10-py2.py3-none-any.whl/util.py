""" Utility functions for traceguide.instrument package
"""
import uuid
import time
import traceguide.constants as constants

def _service_url_from_hostport(secure, host, port):
    """ Create appropriate service service URL.
        Note: Currently, https does not work for lcoalhost. Though it does work
                work on staging.
    """
    if secure:
        protocol = 'https://'
    else:
        protocol = 'http://'
    return ''.join([protocol, host, ':', str(port), '/_rpc/v1/reports/binary'])

def _generate_guid():
    """ Construct a guid - random 64 bit integer converted to a string.
    """
    # Note: uuid.uuid4() returns 128 bit int. To get 64 bit int, apply the mask.
    guid = uuid.uuid4().int & (1<<64)-1
    return str(guid)

def _now_micros():
    """ Get time in microseconds.
    """
    return int(round(time.time() * constants.SECONDS_TO_MICRO))

def _parse_level_log_kwargs(**kwargs):
    """ Parse kwargs for level logs into a dict.
    """
    parsed_kwargs = {}
    if kwargs is not None:
        for key, val in kwargs.iteritems():
            if key == constants.PAYLOAD:
                parsed_kwargs[constants.PAYLOAD] = val
            elif key == constants.span_guid:
                parsed_kwargs[constants.span_guid] = val
    return parsed_kwargs