import re
from lingua.extractors import Message
from lingua.extractors import Extractor

REGEX_MSG = r'''%s\(("(?:\\"|[^"])*"|'(?:\\'|[^'])*')[\s\n]*,[\s\n]*("(?:\\"|[^"])*"|'(?:\\'|[^'])*')'''
REGEX_FACTORY = re.compile(r'''(\w(?:\w|[0-9])*)[\s\n]*=[\s\n]*i18n[\s\n]*\([\s\n]*("(?:\\"|[^"])*"|'(?:\\'|[^'])*')[\s\n]*\)''')


class ExtjsExtractor(Extractor):
    '''Extjs sources'''

    extensions = ['.js']

    def __call__(self, filename, options, fileobj=None, lineno=0):
        factories = list()
        trim = lambda x: x[1:-1]
        with open(filename, 'r+') as f:
            data = f.read()
        for match in REGEX_FACTORY.finditer(data):
            var, domain = match.groups()
            domain = trim(domain)
            if options.domain is None or options.domain == domain:
                factories.append(var)

        # pre calculation to now with lineno the string was found
        s = 0
        linesum = list()
        for line in data.split('\n'):
            s += len(line)
            linesum.append(s)
        for factory in factories:
            regex = re.compile(REGEX_MSG % factory)
            for match in regex.finditer(data):
                msgid, default = match.groups()
                msgid, default = trim(msgid), trim(default)

                # calculate lineno
                start = match.start()
                for i, s in enumerate(linesum):
                    lineno = i + 1
                    if start < s:
                        break

                yield Message(None, msgid, None, [],
                              'Default: %s' % default, '', (filename, lineno))
