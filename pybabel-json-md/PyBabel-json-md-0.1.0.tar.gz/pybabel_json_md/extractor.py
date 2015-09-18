from babel.messages.jslexer import tokenize, unquote_string


NAME_LIST = []


class JsonExtractorMD(object):
    def __init__(self, data):
        self.data = data
        self.current_key = None
        self.prev_token = None

        self.processing_list = False
        self.first_token_in_list = None

        self.results = []

    def add_result(self, token):
        if self.is_keepable():
            result = dict(
                line_number=token.lineno,
                function=u'gettext',
                value=[unquote_string(token.value)]
            )
            self.results.append(result)

    def is_keepable(self):
        global NAME_LIST

        if not NAME_LIST:
            return True
        elif self.current_key in NAME_LIST:
            return True

        return False

    def add_first_token_in_list(self):
        if self.first_token_in_list:
            self.add_result(self.first_token_in_list)
            self.first_token_in_list = None

    def tokenized_results(self):
        """
        Returns a list of dict items:
            {line_number, function, value}
            for the valid strings found in the file.
        The basic logic is to handle:
            Key:Value pairs,
            Lists of string values (1 to n) and
            Lists of List of string values (1 to n).

        Note 1: The function is always gettext. The value will be a tuple of
                the matching string.
        Note 2: The same string value could appear in multiple lines within a
                a JSON file. The returned list will contain each occurrence.
        """

        encoding = 'utf-8'

        for token in tokenize(self.data.decode(encoding)):
            if token.type == u'operator':
                if token.value == ']':
                    self.add_first_token_in_list()
                    self.processing_list = False
            elif token.type == u'string':
                if (self.prev_token.type == u'operator' and
                        self.prev_token.value == ':'):
                    self.add_result(token)
                elif (self.prev_token.type == u'operator' and
                        self.prev_token.value == '['):
                    if self.processing_list:
                        self.current_key = unquote_string(
                            self.first_token_in_list.value)
                    else:
                        self.processing_list = True
                    self.first_token_in_list = token
                elif self.processing_list:
                    self.add_first_token_in_list()
                    self.add_result(token)
                else:
                    self.current_key = unquote_string(token.value)
            self.prev_token = token

        return self.results


def __handle_option_name_list(options):
    global NAME_LIST
    if not NAME_LIST:
        name_list = options.pop('name_list', None)
        if name_list:
            NAME_LIST = [x.strip() for x in name_list.split(',')]


def __handle_options(options):
    if options:
        __handle_option_name_list(options)


def extract_json_md(fileobj, keywords, comment_tags, options):
    """
    Extracts all 'value' strings within a metadef JSON file for all keys.
    The key name could be to a list of strings (e.g., 'enum': [list]).
    However, if the option 'name_list' is specified in babel.cfg then
    just the strings for the key names in the name_list will be returned.
    """
    __handle_options(options)

    data = fileobj.read()
    json_extractor = JsonExtractorMD(data)
    results = json_extractor.tokenized_results()

    for item in results:
        yield (item['line_number'],
               item['function'],
               item['value'], [])
