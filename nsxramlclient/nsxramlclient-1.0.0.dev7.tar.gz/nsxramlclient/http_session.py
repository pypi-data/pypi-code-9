__author__ = 'yfauser'

import requests
import xml.dom.minidom as md
import sys
from collections import OrderedDict
import xmloperations
from lxml import etree as et


class Session(object):
    def __init__(self, username='admin', password='default', debug=False, verify=False, suppress_warnings=False):
        self._username = username
        self._password = password
        self._debug = debug
        self._verify = verify
        self._suppress_warnings = suppress_warnings
        self._session = requests.Session()
        self._session.verify = self._verify
        self._session.auth = (self._username, self._password)

        # if debug then enable underlying httplib debugging
        if self._debug:
            import httplib
            httplib.HTTPConnection.debuglevel = 1

        # if suppress_warnings then disable any InsecureRequestWarnings caused by self signed certs
        if self._suppress_warnings:
            requests.packages.urllib3.disable_warnings()

    def do_request(self, method, url, data=None, headers=None, params=None):
        """
        Handle API requests / responses transport

        :param method: HTTP method to use as string
        :param data: Any data as PyDict (will be converted to XML string)
        :param headers: Any data as PyDict
        :return: If response is XML then an xml.etree.ElementTree else the raw content
        :raise: Any unsuccessful HTTP response code
        """

        response_content = None
        if data:
            if headers:
                headers.update({'Content-Type': 'application/xml'})
            else:
                headers = {'Content-Type': 'application/xml'}

            if self._debug:
                print md.parseString(data).toprettyxml()

        response = self._session.request(method, url, headers=headers, params=params, data=data)

        if response.status_code not in [200, 201, 204]:
            if 'content-type' in response.headers:
                if response.headers['content-type'].find('text/html') != -1:
                    response_content = self._html2text(response.content)
                elif response.headers['content-type'].find('application/xml') != -1:
                    response_content = xmloperations.pretty_xml(response.content)
                else:
                    response_content = response.content
            else:
                response_content = response.content

            sys.exit('receive bad status code {}\n{}'.format(response.status_code, response_content))

        elif 'content-type' in response.headers:
            if response.headers['content-type'].find('application/xml') != -1:
                response_content = xmloperations.xml_to_dict(et.fromstring(response.content))
            else:
                response_content = response.content

        response_odict = OrderedDict([('status', response.status_code), ('body', response_content),
                                      ('location', None), ('objectId', None), ('Etag', None)])

        if 'location' in response.headers:
            response_odict['location'] = response.headers['location']
            response_odict['objectId'] = response.headers['location'].split('/')[-1]

        if 'Etag' in response.headers:
            response_odict['Etag'] = response.headers['Etag']

        return response_odict

    def _html2text(self, strText):
        str1 = strText
        int2 = str1.lower().find("<body")
        if int2 > 0:
           str1 = str1[int2:]
        int2 = str1.lower().find("</body>")
        if int2 > 0:
           str1 = str1[:int2]
        list1 = ['<br>',  '<tr',  '<td', '</p>', 'span>', 'li>', '</h', 'div>' ]
        list2 = [chr(13), chr(13), chr(9), chr(13), chr(13),  chr(13), chr(13), chr(13)]
        bolFlag1 = True
        bolFlag2 = True
        strReturn = ""
        for int1 in range(len(str1)):
          str2 = str1[int1]
          for int2 in range(len(list1)):
            if str1[int1:int1+len(list1[int2])].lower() == list1[int2]:
               strReturn = strReturn + list2[int2]
          if str1[int1:int1+7].lower() == '<script' or str1[int1:int1+9].lower() == '<noscript':
             bolFlag1 = False
          if str1[int1:int1+6].lower() == '<style':
             bolFlag1 = False
          if str1[int1:int1+7].lower() == '</style':
             bolFlag1 = True
          if str1[int1:int1+9].lower() == '</script>' or str1[int1:int1+11].lower() == '</noscript>':
             bolFlag1 = True
          if str2 == '<':
             bolFlag2 = False
          if bolFlag1 and bolFlag2 and (ord(str2) != 10) :
            strReturn = strReturn + str2
          if str2 == '>':
             bolFlag2 = True
          if bolFlag1 and bolFlag2:
            strReturn = strReturn.replace(chr(32)+chr(13), chr(13))
            strReturn = strReturn.replace(chr(9)+chr(13), chr(13))
            strReturn = strReturn.replace(chr(13)+chr(32), chr(13))
            strReturn = strReturn.replace(chr(13)+chr(9), chr(13))
            strReturn = strReturn.replace(chr(13)+chr(13), chr(13))
        strReturn = strReturn.replace(chr(13), '\n')
        return strReturn





