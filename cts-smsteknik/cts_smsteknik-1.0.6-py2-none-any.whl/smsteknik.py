#!/usr/bin/env python
# encoding: utf-8
"""
Copyright (c) 2014 Cross Technology AB

"""
from __future__ import unicode_literals
import urllib
from .exc import *
from xml.sax.saxutils import escape as xml_escape

class SMSTeknikClient(object):
    """
    Client for the SMS Teknik Gateway API.

    Parameters:
        id (str): Company name
        user (str): Account username
        password (str): Account password

    Other Parameters:
        deliverystatusaddress (str): Email or URL for report
        deliverystatustype (str): Delivery report method

            'off'  - No delivery status (Default)

            'email' - Email

            'get' - HTTP GET

            'post' - HTTP POST

            'xml' - HTTP XML

        smssender (str): Sender shown to recipients
        multisms (bool): Allow message splitting (Supported on most modern phones)
        url (str): API URL, (Default: https://www.smsteknik.se/Member/SMSConnectDirect/SendSMSv3.asp )

    Example:
        >>> client = SMSTeknikClient(id=..., user=..., password=..., ...)
        >>> client.send(['+4673XXXXXXX', '+46707XXXXXX'], 'Hello Wörld!')
        [
            { 'number': '+4673XXXXXXX', 'SMSID': 01234 },
            { 'number': '+46707XXXXXX', 'SMSID': 49312 }
        ]
    
    """

    _errors = {
            'Access denied': AccessDenied,
            'No SMS left':  NoSMSLeft,
            'Parse error':  ParseError,
            'The required XML-tag <udmessage> is missing': ParseError,
            # Yes, the typo is actually in the API
            "Message could't be empty": EmptyMessage,
            'Invalid phonenumber':      InvalidPhonenumber,
            'Number is blocked':        BlockedNumber
            }


    _deliverystatustype_name = {
            None: 0,
            'off': 0,
            'email': 1,
            'get': 2,
            'post': 3,
            'xml': 4}

    # Consult the Manual for specifications on the XML
    _xml_template = """<?xml version="1.0" encoding="utf-8" ?>
        <sms-teknik>
            <operationtype>0</operationtype>
            <flash>0</flash>
            <multisms>{multisms}</multisms>
            <maxmultisms>0</maxmultisms>
            <compresstext>0</compresstext>
            <udmessage><![CDATA[{message}]]></udmessage>
            <smssender>{smssender}</smssender>
            <deliverystatustype>{deliverystatustype}</deliverystatustype>
            <deliverystatusaddress>{deliverystatusaddress}</deliverystatusaddress>
            <usereplynumber>{usereplynumber}</usereplynumber>
            <usereplyforwardtype>{usereplyforwardtype}</usereplyforwardtype>
            <usereplyforwardurl>{usereplyforwardurl}</usereplyforwardurl>
            <usereplycustomid></usereplycustomid>
            <usee164>0</usee164>
            <items>        
                {items}
            </items>        
        </sms-teknik>"""

    _recipients_template = """
        <recipient>
            <orgaddress>{recipient}</orgaddress> 
        </recipient>
    """

    _default_options = {
        'id': None,
        'user': None,
        'password': None,
        'deliverystatustype': 0,
        'deliverystatusaddress': '',
        'usereplynumber': 0,
        'usereplyforwardtype': 0,
        'usereplyforwardurl': '',
        'smssender': '',
        'multisms': 1,
        'url': 'https://www.smsteknik.se/Member/SMSConnectDirect/SendSMSv3.asp'}

    def __init__(self, **kwargs):
        """SMSTeknik interface
        """
        self.options = {opt: kwargs.get(opt, default)
            for (opt, default) in self._default_options.iteritems()}

        self.options['deliverystatustype'] = self._deliverystatustype_name.get(
                self.options['deliverystatustype'],
                self.options['deliverystatustype'])

        intopts = ['deliverystatustype', 'usereplynumber', 'usereplyforwardtype', 'multisms']
        for key in intopts:
            self.options[key] = int(self.options[key])

        required = ['id', 'user', 'password']
        for key in required:
            if self.options[key] is None:
                raise ValueError("Missing argument: {}".format(key))

    def _recipient_entry(self, recipient):
        '''
        Create xml for recipient

        Parameters:
            recipient (string): Number
        '''
        return self._recipients_template.format(
                recipient=xml_escape(recipient)
                )

    def send(self, recipients, message):
        """
        Send an SMS

        Raises `SMSTeknikError` if the API gives less responses than there
        are recipients.

        Parameters:
            recipients (list): Phone numbers
            message (str): Message to send

        Returns:
            list: dicts with number, SMSID and possibly error


        Example:

            >>> client.send(['123 456', 'not a number'], 'hi.')
            [
                {'number': '123 456', 'SMSID': 0000},
                {'number': 'not a number', 'SMSID': None, 'error': InvalidPhonenumber('Invalid phonenumber #not a number#')}
             ]

        """
        if not (self.options['multisms'] == 1) and len(message) > 160:
            raise ValueError("Max SMS size is 160 characters")

        items = [self._recipient_entry(r) for r in recipients]

        xml = self._xml_template.format(
            message = message,
            items   = '\n'.join(items),
            **self.options
        )

        # Create the URL used for POSTing the XML
        url = "{url}?id={quoted_id}&user={user}&pass={password}".format(
                quoted_id=urllib.quote_plus(self.options['id']),
                **self.options
        )

        # Call the Gateway API with the XML as POST-data
        f = urllib.urlopen(url, xml.encode('utf-8'))
        raw_results = f.read().split(';')

        if len(raw_results) != len(recipients):
            # Not same number of results as recipients
            # wont be able to parse the result properly
            error = self._get_error(raw_results[0])
            if error is None:
                raise SMSTeknikError(raw_results)
            else:
                raise error

        results = self._parse_result(raw_results, recipients)

        return results

    def _parse_result(self, result, recipients):
        """
        Parse the semi-colon separated status responses

        Returns a list of dicts with 'number' and 'SMSID' for each recipient
        If the send failed the 'SMSID' will be None and there will be an
        'error' item with the corresponding exception as defined in the Gateway API
        in the call to _get_error()

        Note that the exceptions are not raised.
        """
        parsed = []
        for number, entry in zip(recipients, result):
            error = self._get_error(entry)
            if error is None:
                parsed.append({'number': number, 'SMSID': entry})
            else:
                parsed.append({'number': number, 'SMSID': None, 'error': error})
        return parsed

    def _get_error(self, err_code):
        """
        Returns exception corresponding to error code, or None
        if it was a normal condition (just numbers)
        """
        if err_code.isdigit():
            # Normal condition, just an SMSID
            return None

        err_msg = err_code.split(':')[-1]
        for err_start, exc in self._errors.iteritems():
            if err_msg.startswith(err_start):
                return exc(err_msg)

        # Unknown error, return the generic error
        return SMSTeknikError(err_msg)
