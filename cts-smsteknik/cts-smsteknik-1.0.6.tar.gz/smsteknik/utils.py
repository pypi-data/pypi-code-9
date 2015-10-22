#!/usr/bin/env python
# coding: utf-8
from __future__ import unicode_literals

STATE_FAILED = ('EXPIRED', 'UNDELIV', 'REJECTED', 'FAILED')
def parse_mail(body):
    '''
    Parse an email status report from SMSTeknik

    The returned status is 'sent' unless there
    is enough information to know it is either
    'delivered' or 'failed'

    Does not decode UTF-7.

    Only the first line of long messages is returned

    Parameters:
        body (str): Mail body

    Returns:
        dict: Delivery information

    Example:
        Parse the body of a mail:

            >>> parse_email("""2014-09-24 13:25:05
            ... Nr:  46701234
            ... RefID: 1111
            ... State: DELIVRD
            ... DateTime: 2014-09-24 13:25:03
            ... Text: <abc> Hello Wörld & Sånt!
            ... """)
            {
                "number":   '46701234',
                "SMSID":    '1111',
                "status":   'delivered',
                "date":     '2014-09-24 13:25:03',
                "text":     '<abc> Hello Wörld & Sånt!'
            }
    '''

    # Ignore the first line with a date
    rows = body.strip().splitlines()[1:]

    # Very simplified parsing, causing long texts to get cropped
    # (and noice to get in if there are long texts with ':' )
    content = dict([r.split(':', 1) for r in rows if ':' in r])
    for k in content:
        content[k] = content[k].strip()

    status = 'sent'
    if content['State'] == 'DELIVRD':
        status = 'delivered'
    elif content['State'] in STATE_FAILED:
        status = 'failed'

    parsed = {
        'number': content['Nr'],
        'SMSID':  content['RefID'],
        'date':   content['DateTime'],
        'text':   content['Text'],
        'status':  status
    }

    return parsed


