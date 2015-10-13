#!/usr/bin/env python
# encoding=utf8
# The spec xml file parser

"""The spec xml file parser

Used to parse mime types spec from http://www.iana.org/assignments/media-types/media-types.xhtml

The latest xml spec file: http://www.iana.org/assignments/media-types/media-types.xml

"""

import sys
reload(sys)
sys.setdefaultencoding('utf8')

import re

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

import requests

DEFAULT_LATEST_XML_URL = 'http://www.iana.org/assignments/media-types/media-types.xml'
SUB_REGEX = re.compile('\([^\)]*\)')

class Parser(object):
    """The parser
    """
    def parse(self, text):
        """Parse the text content
        """
        root = ET.fromstring(text)
        for elm in root.findall('{http://www.iana.org/assignments}registry'):
            for record in elm.findall('{http://www.iana.org/assignments}record'):
                for fileElm in record.findall('{http://www.iana.org/assignments}file'):
                    if fileElm.get('type') == 'template':
                        mimeType = fileElm.text.strip()
                        yield mimeType
                        break

    def parsefile(self, filename):
        """Parse from the file
        """
        with open(filename, 'rb') as fd:
            return self.parse(fd.read())

    def latest(self, url = None):
        """Get the latest spec and parse
        """
        rsp = requests.get(url or DEFAULT_LATEST_XML_URL)
        return self.parse(rsp.content)

def getPythonVarName(name):
    """Get the python variable name
    """
    return SUB_REGEX.sub('', name.replace('+', '_').replace('-', '_').replace('.', '_').replace(' ', '').replace('/', '_')).upper()

if __name__ == '__main__':

    from argparse import ArgumentParser

    def getArguments():
        """Get arguments
        """
        parser = ArgumentParser(description = 'Mimetype parsing tool')
        subParsers = parser.add_subparsers(dest = 'type')
        # Latest parser
        latestParser = subParsers.add_parser('latest')
        latestParser.add_argument('--url', dest = 'url', help = 'The xml url')
        latestParser.add_argument('--of', dest = 'outputFormat', default = 'text', choices = [ 'text', 'python' ], help = 'The output format')
        latestParser.add_argument('-o', '--output', dest = 'output', default = '-', help = 'The output file. - means stdout')
        # File parser
        fileParser = subParsers.add_parser('file')
        fileParser.add_argument('-i', '--input', dest = 'input', required = True, help = 'Xml file')
        fileParser.add_argument('--of', dest = 'outputFormat', default = 'text', choices = [ 'text', 'python' ], help = 'The output format')
        fileParser.add_argument('-o', '--output', dest = 'output', default = '-', help = 'The output file. - means stdout')
        # Done
        return parser.parse_args()

    def main():
        """The main entry
        """
        args = getArguments()
        parser = Parser()
        if args.type == 'latest':
            # The latest
            mimeTypes = parser.latest(args.url)
        else:
            # The file
            mimeTypes = parser.parsefile(args.input)
        # Output
        if args.output == '-':
            out = sys.stdout
        else:
            out = open(args.output, 'wb')
        if args.outputFormat == 'text':
            for typename in mimeTypes:
                print >>out, typename
        else:
            print >>out, '''# encoding=utf8'
# The auto-generated mimetypes

"""The auto-generated mimetypes
"""
'''
            for typename in mimeTypes:
                name = getPythonVarName(typename)
                print >>out, '{:<64}= \'{}\''.format(name, typename)

    main()

